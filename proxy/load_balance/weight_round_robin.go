package load_balance

import (
	"errors"
	"strconv"
	"fmt"
	"strings"
	"sync"
)

type WeightRoundRobinBalance struct {
	curIndex int
	rsw []string
	rss []*WeightNode
	conf LoadBalanceConf
	mux sync.RWMutex
}

type WeightNode struct {
	addr string
	weight int
	effectiveWeight int
	currentWeight int
}

func (r *WeightRoundRobinBalance) Add(params ...string) error {
	if len(params) != 2 {
		return errors.New("param len need 2")
	}
	parInt, err := strconv.ParseInt(params[1], 10, 64)
	if err != nil {
		return err
	}
	
	r.mux.Lock()
	defer r.mux.Unlock()
	
	curNode := &WeightNode{
		addr: params[0],
		weight: int(parInt),
	}
	curNode.effectiveWeight = curNode.weight
	r.rss = append(r.rss, curNode)
	return nil
}

func (r *WeightRoundRobinBalance) Next() string {
	r.mux.Lock()
	defer r.mux.Unlock()
	
	if len(r.rss) == 0 {
		return ""
	}
	
	total := 0
	var best *WeightNode
	for i := 0; i < len(r.rss); i++ {
		w := r.rss[i]
		// 1. 统计总权重
		total += w.effectiveWeight
		// 2.临时权重变更
		w.currentWeight += w.effectiveWeight
		// 3.有效权重
		if w.effectiveWeight < w.weight {
			w.effectiveWeight++
		}
		if best == nil || w.currentWeight > best.currentWeight {
			best = w
		}
	}
	if best == nil {
		return ""
	}
	best.currentWeight -= total
	return best.addr
}

func (r *WeightRoundRobinBalance) Get(key string) (string, error) {
	return r.Next(), nil
}

func (r *WeightRoundRobinBalance) SetConf(conf LoadBalanceConf) {
	r.mux.Lock()
	defer r.mux.Unlock()
	r.conf = conf
}

func (r *WeightRoundRobinBalance) Update() {
	r.mux.Lock()
	defer r.mux.Unlock()
	
	if conf, ok := r.conf.(*LoadBalanceZkConf); ok {
		if debugMode {
			fmt.Println("WeightRoundRobinBalance get conf:", conf.GetConf())
		}
		// Clear and rebuild the node list
		r.rss = r.rss[:0] // Keep capacity, reset length
		for _, ip := range conf.GetConf() {
			parts := strings.Split(ip, ",")
			if len(parts) >= 2 {
				// Internal call doesn't need mutex as we already hold it
				r.addInternal(parts[0], parts[1])
			}
		}
	}
	if conf, ok := r.conf.(*LoadBalanceCheckConf); ok {
		if debugMode {
			fmt.Println("WeightRoundRobinBalance get conf:", conf.GetConf())
		}
		r.rss = r.rss[:0]
		for _, ip := range conf.GetConf() {
			parts := strings.Split(ip, ",")
			if len(parts) >= 2 {
				r.addInternal(parts[0], parts[1])
			}
		}
	}
}

// Internal add method that doesn't acquire mutex (assumes caller has it)
func (r *WeightRoundRobinBalance) addInternal(addr, weightStr string) error {
	parInt, err := strconv.ParseInt(weightStr, 10, 64)
	if err != nil {
		return err
	}
	
	curNode := &WeightNode{
		addr: addr,
		weight: int(parInt),
	}
	curNode.effectiveWeight = curNode.weight
	r.rss = append(r.rss, curNode)
	return nil
}