package zookeeper

import (
	"fmt"
	"github.com/samuel/go-zookeeper/zk"
	"log"
	"sync"
	"time"
)

var (
	// Connection pool for ZooKeeper connections
	zkPool = &sync.Pool{
		New: func() interface{} {
			return nil
		},
	}
	zkPoolMux sync.RWMutex
	globalHosts []string
	
	// Debug mode control
	debugMode = false
)

// SetDebugMode enables or disables debug logging
func SetDebugMode(enabled bool) {
	debugMode = enabled
}

type ZkManager struct {
	hosts      []string
	conn       *zk.Conn
	pathPrefix string
	logger     *log.Logger
}

func NewZkManager(hosts []string) *ZkManager {
	zkPoolMux.Lock()
	globalHosts = hosts
	zkPoolMux.Unlock()
	
	return &ZkManager{
		hosts: hosts, 
		pathPrefix: "/gateway_servers_",
		logger: log.New(log.Writer(), "[ZK] ", log.LstdFlags),
	}
}

//连接zk服务器
func (z *ZkManager) GetConnect() error {
	// Try to get connection from pool first
	if poolConn := zkPool.Get(); poolConn != nil {
		if conn, ok := poolConn.(*zk.Conn); ok && conn.State() == zk.StateHasSession {
			z.conn = conn
			return nil
		}
	}
	
	// Create new connection with optimized settings
	conn, _, err := zk.Connect(z.hosts, 10*time.Second, zk.WithEventCallback(z.eventCallback))
	if err != nil {
		return fmt.Errorf("failed to connect to ZooKeeper: %w", err)
	}
	z.conn = conn
	return nil
}

// Event callback for connection monitoring
func (z *ZkManager) eventCallback(event zk.Event) {
	switch event.State {
	case zk.StateDisconnected:
		if debugMode {
			z.logger.Printf("ZooKeeper disconnected: %v", event)
		}
	case zk.StateConnected:
		if debugMode {
			z.logger.Printf("ZooKeeper connected: %v", event)
		}
	case zk.StateExpired:
		z.logger.Printf("ZooKeeper session expired: %v", event)
		// Reconnect on session expiration
		go z.reconnect()
	}
}

// Reconnect logic for session expiration
func (z *ZkManager) reconnect() {
	time.Sleep(1 * time.Second) // Brief delay before reconnection
	if err := z.GetConnect(); err != nil {
		z.logger.Printf("Failed to reconnect to ZooKeeper: %v", err)
	}
}

//关闭服务
func (z *ZkManager) Close() {
	if z.conn != nil {
		// Return healthy connections to the pool
		if z.conn.State() == zk.StateHasSession {
			zkPool.Put(z.conn)
		} else {
			z.conn.Close()
		}
		z.conn = nil
	}
}

//获取配置
func (z *ZkManager) GetPathData(nodePath string) ([]byte, *zk.Stat, error) {
	if z.conn == nil {
		return nil, nil, fmt.Errorf("no ZooKeeper connection")
	}
	return z.conn.Get(nodePath)
}

//更新配置
func (z *ZkManager) SetPathData(nodePath string, config []byte, version int32) error {
	if z.conn == nil {
		return fmt.Errorf("no ZooKeeper connection")
	}
	
	ex, _, _ := z.conn.Exists(nodePath)
	if !ex {
		_, err := z.conn.Create(nodePath, config, 0, zk.WorldACL(zk.PermAll))
		return err
	}
	
	_, dStat, err := z.GetPathData(nodePath)
	if err != nil {
		return fmt.Errorf("failed to get path data: %w", err)
	}
	
	_, err = z.conn.Set(nodePath, config, dStat.Version)
	if err != nil {
		return fmt.Errorf("failed to update node: %w", err)
	}
	
	if debugMode {
		z.logger.Printf("SetData successful for path: %s", nodePath)
	}
	return nil
}

//创建临时节点
func (z *ZkManager) RegistServerPath(nodePath, host string) error {
	if z.conn == nil {
		return fmt.Errorf("no ZooKeeper connection")
	}
	
	ex, _, err := z.conn.Exists(nodePath)
	if err != nil {
		return fmt.Errorf("exists check failed for %s: %w", nodePath, err)
	}
	
	if !ex {
		//持久化节点，思考题：如果不是持久化节点会怎么样？
		_, err = z.conn.Create(nodePath, nil, 0, zk.WorldACL(zk.PermAll))
		if err != nil {
			return fmt.Errorf("create failed for %s: %w", nodePath, err)
		}
	}
	
	//临时节点
	subNodePath := nodePath + "/" + host
	ex, _, err = z.conn.Exists(subNodePath)
	if err != nil {
		return fmt.Errorf("exists check failed for %s: %w", subNodePath, err)
	}
	
	if !ex {
		_, err = z.conn.Create(subNodePath, nil, zk.FlagEphemeral, zk.WorldACL(zk.PermAll))
		if err != nil {
			return fmt.Errorf("create ephemeral node failed for %s: %w", subNodePath, err)
		}
	}
	return nil
}

//获取服务列表
func (z *ZkManager) GetServerListByPath(path string) ([]string, error) {
	if z.conn == nil {
		return nil, fmt.Errorf("no ZooKeeper connection")
	}
	
	list, _, err := z.conn.Children(path)
	if err != nil {
		return nil, fmt.Errorf("failed to get children for %s: %w", path, err)
	}
	return list, nil
}

//watch机制，服务器有断开或者重连，收到消息
func (z *ZkManager) WatchServerListByPath(path string) (chan []string, chan error) {
	snapshots := make(chan []string, 10) // Buffered channel for better performance
	errors := make(chan error, 10)       // Buffered error channel
	
	go func() {
		defer close(snapshots)
		defer close(errors)
		
		for {
			if z.conn == nil {
				errors <- fmt.Errorf("no ZooKeeper connection")
				return
			}
			
			snapshot, _, events, err := z.conn.ChildrenW(path)
			if err != nil {
				errors <- fmt.Errorf("ChildrenW failed: %w", err)
				return
			}
			
			select {
			case snapshots <- snapshot:
			case <-time.After(5 * time.Second):
				if debugMode {
					z.logger.Printf("Timeout sending snapshot for path: %s", path)
				}
			}
			
			select {
			case evt := <-events:
				if evt.Err != nil {
					errors <- fmt.Errorf("watch event error: %w", evt.Err)
					return
				}
				if debugMode {
					z.logger.Printf("ChildrenW Event Path:%v, Type:%v", evt.Path, evt.Type)
				}
			case <-time.After(30 * time.Second):
				// Timeout protection
				if debugMode {
					z.logger.Printf("Watch timeout for path: %s", path)
				}
			}
		}
	}()

	return snapshots, errors
}

//watch机制，监听节点值变化
func (z *ZkManager) WatchPathData(nodePath string) (chan []byte, chan error) {
	snapshots := make(chan []byte, 10)
	errors := make(chan error, 10)

	go func() {
		defer close(snapshots)
		defer close(errors)
		
		for {
			if z.conn == nil {
				errors <- fmt.Errorf("no ZooKeeper connection")
				return
			}
			
			dataBuf, _, events, err := z.conn.GetW(nodePath)
			if err != nil {
				errors <- fmt.Errorf("GetW failed: %w", err)
				return
			}
			
			select {
			case snapshots <- dataBuf:
			case <-time.After(5 * time.Second):
				if debugMode {
					z.logger.Printf("Timeout sending data snapshot for path: %s", nodePath)
				}
			}
			
			select {
			case evt := <-events:
				if evt.Err != nil {
					errors <- fmt.Errorf("watch data event error: %w", evt.Err)
					return
				}
				if debugMode {
					z.logger.Printf("GetW Event Path:%v, Type:%v", evt.Path, evt.Type)
				}
			case <-time.After(30 * time.Second):
				if debugMode {
					z.logger.Printf("Watch data timeout for path: %s", nodePath)
				}
			}
		}
	}()
	return snapshots, errors
}