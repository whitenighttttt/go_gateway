package zookeeper

import (
	"fmt"
	"github.com/samuel/go-zookeeper/zk"
	"sync"
	"time"
)

type ZkManager struct {
	hosts      []string
	conn       *zk.Conn
	pathPrefix string
	mutex      sync.RWMutex
	connected  bool
}

func NewZkManager(hosts []string) *ZkManager {
	return &ZkManager{hosts: hosts, pathPrefix: "/gateway_servers_"}
}

//连接zk服务器
func (z *ZkManager) GetConnect() error {
	z.mutex.Lock()
	defer z.mutex.Unlock()
	
	if z.connected && z.conn != nil {
		return nil // Already connected
	}
	
	conn, _, err := zk.Connect(z.hosts, 5*time.Second)
	if err != nil {
		return err
	}
	z.conn = conn
	z.connected = true
	return nil
}

//关闭服务
func (z *ZkManager) Close() {
	z.mutex.Lock()
	defer z.mutex.Unlock()
	
	if z.conn != nil {
		z.conn.Close()
		z.conn = nil
		z.connected = false
	}
}

//获取配置
func (z *ZkManager) GetPathData(nodePath string) ([]byte, *zk.Stat, error) {
	if err := z.ensureConnection(); err != nil {
		return nil, nil, err
	}
	
	z.mutex.RLock()
	defer z.mutex.RUnlock()
	
	return z.conn.Get(nodePath)
}

//更新配置
func (z *ZkManager) SetPathData(nodePath string, config []byte, version int32) (err error) {
	if err := z.ensureConnection(); err != nil {
		return err
	}
	
	z.mutex.Lock()
	defer z.mutex.Unlock()
	
	ex, _, _ := z.conn.Exists(nodePath)
	if !ex {
		z.conn.Create(nodePath, config, 0, zk.WorldACL(zk.PermAll))
		return nil
	}
	_, dStat, err := z.GetPathData(nodePath)
	if err != nil {
		return
	}
	_, err = z.conn.Set(nodePath, config, dStat.Version)
	if err != nil {
		fmt.Println("Update node error", err)
		return err
	}
	fmt.Println("SetData ok")
	return
}

//创建临时节点
func (z *ZkManager) RegistServerPath(nodePath, host string) (err error) {
	if err := z.ensureConnection(); err != nil {
		return err
	}
	
	z.mutex.Lock()
	defer z.mutex.Unlock()
	
	ex, _, err := z.conn.Exists(nodePath)
	if err != nil {
		fmt.Println("Exists error", nodePath)
		return err
	}
	if !ex {
		//持久化节点，思考题：如果不是持久化节点会怎么样？
		_, err = z.conn.Create(nodePath, nil, 0, zk.WorldACL(zk.PermAll))
		if err != nil {
			fmt.Println("Create error", nodePath)
			return err
		}
	}
	//临时节点
	subNodePath := nodePath + "/" + host
	ex, _, err = z.conn.Exists(subNodePath)
	if err != nil {
		fmt.Println("Exists error", subNodePath)
		return err
	}
	if !ex {
		_, err = z.conn.Create(subNodePath, nil, zk.FlagEphemeral, zk.WorldACL(zk.PermAll))
		if err != nil {
			fmt.Println("Create error", subNodePath)
			return err
		}
	}
	return
}

//获取服务列表
func (z *ZkManager) GetServerListByPath(path string) (list []string, err error) {
	if err := z.ensureConnection(); err != nil {
		return nil, err
	}
	
	z.mutex.RLock()
	defer z.mutex.RUnlock()
	
	list, _, err = z.conn.Children(path)
	return
}

//watch机制，服务器有断开或者重连，收到消息
func (z *ZkManager) WatchServerListByPath(path string) (chan []string, chan error) {
	if err := z.ensureConnection(); err != nil {
		errors := make(chan error, 1)
		errors <- err
		return make(chan []string), errors
	}
	
	z.mutex.RLock()
	conn := z.conn
	z.mutex.RUnlock()
	
	snapshots := make(chan []string, 10) // Buffered channel for better performance
	errors := make(chan error, 10)       // Buffered channel for better performance
	
	go func() {
		defer func() {
			close(snapshots)
			close(errors)
		}()
		
		for {
			snapshot, _, events, err := conn.ChildrenW(path)
			if err != nil {
				select {
				case errors <- err:
				default:
					// Channel full, log error instead
					fmt.Printf("Watch error: %v\n", err)
				}
				return
			}
			
			select {
			case snapshots <- snapshot:
			default:
				// Channel full, skip this update
				fmt.Println("Snapshot channel full, skipping update")
			}
			
			select {
			case evt := <-events:
				if evt.Err != nil {
					select {
					case errors <- evt.Err:
					default:
						fmt.Printf("Event error: %v\n", evt.Err)
					}
					return
				}
				fmt.Printf("ChildrenW Event Path:%v, Type:%v\n", evt.Path, evt.Type)
			}
		}
	}()

	return snapshots, errors
}

//watch机制，监听节点值变化
func (z *ZkManager) WatchPathData(nodePath string) (chan []byte, chan error) {
	if err := z.ensureConnection(); err != nil {
		errors := make(chan error, 1)
		errors <- err
		return make(chan []byte), errors
	}
	
	z.mutex.RLock()
	conn := z.conn
	z.mutex.RUnlock()
	
	snapshots := make(chan []byte, 10) // Buffered channel for better performance
	errors := make(chan error, 10)     // Buffered channel for better performance

	go func() {
		defer func() {
			close(snapshots)
			close(errors)
		}()
		
		for {
			dataBuf, _, events, err := conn.GetW(nodePath)
			if err != nil {
				select {
				case errors <- err:
				default:
					fmt.Printf("Watch data error: %v\n", err)
				}
				return
			}
			
			select {
			case snapshots <- dataBuf:
			default:
				// Channel full, skip this update
				fmt.Println("Data snapshot channel full, skipping update")
			}
			
			select {
			case evt := <-events:
				if evt.Err != nil {
					select {
					case errors <- evt.Err:
					default:
						fmt.Printf("Data event error: %v\n", evt.Err)
					}
					return
				}
				fmt.Printf("GetW Event Path:%v, Type:%v\n", evt.Path, evt.Type)
			}
		}
	}()
	return snapshots, errors
}

// ensureConnection ensures we have a valid connection
func (z *ZkManager) ensureConnection() error {
	z.mutex.RLock()
	if z.connected && z.conn != nil {
		z.mutex.RUnlock()
		return nil
	}
	z.mutex.RUnlock()
	
	return z.GetConnect()
}