package load_balance
import (
	"testing"
	"fmt"
	"strconv"
)
func TestRoundRobin(t *testing.T){
	rb := &RoundRobinBalance{}
	for i:=0;i<10;i++{
		rb.Add("127.0.0.1:800"+strconv.Itoa(i))
		// rb.Add("127.0.0.1:8000")
		// rb.Add("127.0.0.1:8001")
		// rb.Add("127.0.0.1:8002")
	}

	fmt.Println(rb.Next())
	fmt.Println(rb.Next())
	fmt.Println(rb.Next())
	fmt.Println(rb.Next())
}