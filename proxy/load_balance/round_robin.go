package load_balance

import (
	"errors"
	"fmt"
	"strings"
)

type RoundRobinBalance struct {
	curIndex int
	// 当前数组
	rss []string
	// 观察主题
	conf LoadBalanceConf
	// sync.RWMutex
}

func (r *RoundRobinBalance) Add(params ...string)error{
	if len(params)==0{
		return errors.New("params len 0")
	}
	addr := params[0]
	r.rss = append(r.rss, addr)
	return nil	
}

func (r *RoundRobinBalance) Next() string{
	if(len(r.rss)==0){
		return ""
	}
	lens := len(r.rss)
	// fmt.Println("Length", lens)
	nextIndex := (r.curIndex+1)%lens
	// fmt.Println("Next Index", nextIndex)
	r.curIndex = nextIndex
	// fmt.Println("Next Index", r.curIndex)
	return r.rss[r.curIndex]
}

func (r *RoundRobinBalance) Get(key string) (string, error){
	return r.Next(), nil
}

func (r *RoundRobinBalance) SetConf(conf LoadBalanceConf){
	r.conf = conf
}

func (r *RoundRobinBalance) Update(){
	if conf, ok:= r.conf.(*LoadBalanceZkConf); ok{
		fmt.Println("Update get Conf", conf.GetConf())
		r.rss = []string{}
		for _,ip := range conf.GetConf(){
			r.Add(strings.Split(ip,",")...)
		}
	}
	if conf, ok:= r.conf.(*LoadBalanceCheckConf); ok{
		fmt.Println("Update get Conf", conf.GetConf())
		r.rss = nil
		for _,ip:= range conf.GetConf(){
			r.Add(strings.Split(ip,",")...)
		}
	}
}
