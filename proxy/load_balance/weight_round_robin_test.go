package load_balance

import (
	"fmt"
	"testing"
)
func TestWeightRoundRobinBalance(t *testing.T){
	rb := &WeightRoundRobinBalance{}
	rb.Add("127.0.0.1:2001","4")
	rb.Add("127.0.0.1:2002","3")
	rb.Add("127.0.0.1:2003","2")
	rb.Add("127.0.0.1:2004","1")

	fmt.Println(rb.Next())
	fmt.Println(rb.Next())
	fmt.Println(rb.Next())
	fmt.Println(rb.Next())
	fmt.Println(rb.Next())
	fmt.Println(rb.Next())
	fmt.Println(rb.Next())
	fmt.Println(rb.Next())
	fmt.Println(rb.Next())
	fmt.Println(rb.Next())
}