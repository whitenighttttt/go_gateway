package load_balance

import (
	"errors"
	"fmt"
	"strings"
	"sync"
)

type RoundRobinBalance struct {
	curIndex int
	// 当前数组
	rss []string
	// 观察主题
	conf LoadBalanceConf
	// Thread safety
	mux sync.RWMutex
}

func (r *RoundRobinBalance) Add(params ...string) error {
	if len(params) == 0 {
		return errors.New("params len 0")
	}
	addr := params[0]
	
	r.mux.Lock()
	defer r.mux.Unlock()
	
	r.rss = append(r.rss, addr)
	return nil
}

func (r *RoundRobinBalance) Next() string {
	r.mux.Lock()
	defer r.mux.Unlock()
	
	if len(r.rss) == 0 {
		return ""
	}
	lens := len(r.rss)
	r.curIndex = (r.curIndex + 1) % lens
	return r.rss[r.curIndex]
}

func (r *RoundRobinBalance) Get(key string) (string, error) {
	return r.Next(), nil
}

func (r *RoundRobinBalance) SetConf(conf LoadBalanceConf) {
	r.mux.Lock()
	defer r.mux.Unlock()
	r.conf = conf
}

func (r *RoundRobinBalance) Update() {
	r.mux.Lock()
	defer r.mux.Unlock()
	
	if conf, ok := r.conf.(*LoadBalanceZkConf); ok {
		// Use info level logging instead of println in production
		if debugMode {
			fmt.Println("Update get Conf", conf.GetConf())
		}
		// Pre-allocate slice for better performance
		newRss := make([]string, 0, len(conf.GetConf()))
		for _, ip := range conf.GetConf() {
			parts := strings.Split(ip, ",")
			if len(parts) > 0 {
				newRss = append(newRss, parts[0])
			}
		}
		r.rss = newRss
		// Reset index when updating servers
		r.curIndex = 0
	}
	if conf, ok := r.conf.(*LoadBalanceCheckConf); ok {
		if debugMode {
			fmt.Println("Update get Conf", conf.GetConf())
		}
		newRss := make([]string, 0, len(conf.GetConf()))
		for _, ip := range conf.GetConf() {
			parts := strings.Split(ip, ",")
			if len(parts) > 0 {
				newRss = append(newRss, parts[0])
			}
		}
		r.rss = newRss
		r.curIndex = 0
	}
}

// Add debug mode control
var debugMode = false

func SetDebugMode(enabled bool) {
	debugMode = enabled
}
