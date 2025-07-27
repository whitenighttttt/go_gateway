package load_balance

import (
	"errors"
	"fmt"
	"hash/crc32"
	"sort"
	"strconv"
	"strings"
	"sync"
)

type Hash func(data []byte) uint32

type UInt32Slice []uint32

func(s UInt32Slice) Len() int{
	return len(s)
}
func(s UInt32Slice) Less(i, j int)bool{
	return s[i]<s[j]
}
func (s UInt32Slice) Swap(i, j int) {
	s[i], s[j] = s[j], s[i]
}

type ConsistentHashBanlance struct {
	mux      sync.RWMutex
	hash     Hash
	replicas int               //复制因子
	keys     UInt32Slice       //已排序的节点hash切片
	hashMap  map[uint32]string //节点哈希和Key的map,键是hash值，值是节点key

	//观察主体
	conf LoadBalanceConf
}

func NewConsistentHashBanlance(replicas int, fn Hash) *ConsistentHashBanlance {
	m := &ConsistentHashBanlance{
		replicas: replicas,
		hash:     fn,
		hashMap:  make(map[uint32]string),
	}
	if m.hash == nil {
		//最多32位,保证是一个2^32-1环
		m.hash = crc32.ChecksumIEEE
	}
	return m
}

// 验证是否为空
func (c *ConsistentHashBanlance) IsEmpty() bool {
	return len(c.keys) == 0
}

func (c *ConsistentHashBanlance) Add(params...string)error{
	if len(params)==0{
		return nil
	}
	addr := params[0]
	c.mux.Lock()
	defer c.mux.Unlock()
	
	// Pre-allocate slice capacity to avoid multiple allocations
	if cap(c.keys) < len(c.keys)+c.replicas {
		newKeys := make(UInt32Slice, len(c.keys), len(c.keys)+c.replicas)
		copy(newKeys, c.keys)
		c.keys = newKeys
	}
	
	// 结合复制因子计算节点hash值
	for i:=0;i<c.replicas;i++{
		hash := c.hash([]byte(strconv.Itoa(i)+addr))
		c.keys = append(c.keys, hash)
		c.hashMap[hash] = addr
	}
	sort.Sort(c.keys)
	return nil
}

func (c *ConsistentHashBanlance) Get(key string)(string,error){
	if c.IsEmpty(){
		return "",errors.New("node is Empty!")
	}
	hash := c.hash([]byte(key))
	
	c.mux.RLock()
	defer c.mux.RUnlock()
	
	// Optimized binary search with early exit
	idx := sort.Search(len(c.keys), func(i int) bool { 
		return c.keys[i] >= hash 
	})
	
	// 如果查找结果 大于 服务器节点哈希数组的最大索引，表示此时该对象哈希值位于最后一个节点之后，那么放入第一个节点中
	if idx == len(c.keys) {
		idx = 0
	}
	
	return c.hashMap[c.keys[idx]], nil
}

func (c *ConsistentHashBanlance) SetConf(conf LoadBalanceConf) {
	c.conf = conf
}

func (c *ConsistentHashBanlance) Update() {
	if conf, ok := c.conf.(*LoadBalanceZkConf); ok {
		fmt.Println("Update get conf:", conf.GetConf())
		c.mux.Lock()
		defer c.mux.Unlock()
		
		// Clear existing data
		c.keys = c.keys[:0] // Reuse slice instead of setting to nil
		c.hashMap = make(map[uint32]string, len(conf.GetConf())*c.replicas)
		
		for _, ip := range conf.GetConf() {
			c.Add(strings.Split(ip, ",")...)
		}
	}
	if conf, ok := c.conf.(*LoadBalanceCheckConf); ok {
		fmt.Println("Update get conf:", conf.GetConf())
		c.mux.Lock()
		defer c.mux.Unlock()
		
		// Clear existing data
		c.keys = c.keys[:0] // Reuse slice instead of setting to nil
		c.hashMap = make(map[uint32]string, len(conf.GetConf())*c.replicas)
		
		for _, ip := range conf.GetConf() {
			c.Add(strings.Split(ip, ",")...)
		}
	}
}