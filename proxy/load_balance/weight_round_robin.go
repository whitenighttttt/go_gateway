package load_balance
import (
	"errors"
	"strconv"
	"fmt"
	"strings"
)

type WeightRoundRobinBalance struct {
	curIndex int
	rsw []string
	rss []*WeightNode
	conf LoadBalanceConf
}

type WeightNode struct {
	addr string
	weight int
	effectiveWeight int
	currentWeight int
}

func (r *WeightRoundRobinBalance) Add(params ...string) error {
	if(len(params)!=2){
		return errors.New("param len need 2")
	}	
	parInt, err := strconv.ParseInt(params[1],10,64)
	if err !=nil{
		return err
	}
	curNode := &WeightNode{
		addr: params[0],
		weight: int(parInt),
	}
	curNode.effectiveWeight = curNode.weight
	r.rss = append(r.rss, curNode)
	return nil
}

func (r *WeightRoundRobinBalance) Next() string {
	total := 0
	var best *WeightNode
	for i:=0;i<len(r.rss);i++{
		w:= r.rss[i]
		// 1. 统计总权重
		total += w.effectiveWeight
		// 2.临时权重变更
		w.currentWeight += w.effectiveWeight
		// 3.有效权重
		if w.effectiveWeight < w.weight{
			w.effectiveWeight++
		}
		if best == nil || w.currentWeight > best.currentWeight{
			best = w
		}
	}
	if best == nil{
		return ""
	}
	best.currentWeight -= total 
	return best.addr
}

func (r *WeightRoundRobinBalance) Get(key string) (string,error){
	return r.Next(),nil
}

func (r *WeightRoundRobinBalance) SetConf(conf LoadBalanceConf) {
	r.conf = conf
}

func (r *WeightRoundRobinBalance) Update() {
	if conf, ok := r.conf.(*LoadBalanceZkConf); ok {
		fmt.Println("WeightRoundRobinBalance get conf:", conf.GetConf())
		r.rss = nil
		for _, ip := range conf.GetConf() {
			r.Add(strings.Split(ip, ",")...)
		}
	}
	if conf, ok := r.conf.(*LoadBalanceCheckConf); ok {
		fmt.Println("WeightRoundRobinBalance get conf:", conf.GetConf())
		r.rss = nil
		for _, ip := range conf.GetConf() {
			r.Add(strings.Split(ip, ",")...)
		}
	}
}