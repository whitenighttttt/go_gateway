package load_balance

import (
	"strconv"
	"testing"
	"sync"
)

// Benchmark Round Robin
func BenchmarkRoundRobin(b *testing.B) {
	rb := &RoundRobinBalance{}
	for i := 0; i < 10; i++ {
		rb.Add("127.0.0.1:800" + strconv.Itoa(i))
	}
	
	b.ResetTimer()
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			rb.Get("test")
		}
	})
}

// Benchmark Weighted Round Robin
func BenchmarkWeightRoundRobin(b *testing.B) {
	wrr := &WeightRoundRobinBalance{}
	for i := 0; i < 10; i++ {
		wrr.Add("127.0.0.1:800"+strconv.Itoa(i), "50")
	}
	
	b.ResetTimer()
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			wrr.Get("test")
		}
	})
}

// Benchmark Consistent Hash
func BenchmarkConsistentHash(b *testing.B) {
	ch := NewConsistentHashBanlance(150, nil)
	for i := 0; i < 10; i++ {
		ch.Add("127.0.0.1:800" + strconv.Itoa(i))
	}
	
	b.ResetTimer()
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			ch.Get("test-key-" + strconv.Itoa(b.N%1000))
		}
	})
}

// Benchmark Random
func BenchmarkRandom(b *testing.B) {
	rb := &RandomBalance{}
	for i := 0; i < 10; i++ {
		rb.Add("127.0.0.1:800" + strconv.Itoa(i))
	}
	
	b.ResetTimer()
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			rb.Get("test")
		}
	})
}

// Benchmark concurrent access to Round Robin
func BenchmarkRoundRobinConcurrent(b *testing.B) {
	rb := &RoundRobinBalance{}
	for i := 0; i < 10; i++ {
		rb.Add("127.0.0.1:800" + strconv.Itoa(i))
	}
	
	var wg sync.WaitGroup
	numGoroutines := 100
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		wg.Add(numGoroutines)
		for j := 0; j < numGoroutines; j++ {
			go func() {
				defer wg.Done()
				rb.Get("test")
			}()
		}
		wg.Wait()
	}
}

// Benchmark memory allocation patterns
func BenchmarkRoundRobinMemory(b *testing.B) {
	b.ReportAllocs()
	rb := &RoundRobinBalance{}
	for i := 0; i < 10; i++ {
		rb.Add("127.0.0.1:800" + strconv.Itoa(i))
	}
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		rb.Get("test")
	}
}

// Test load balancer factory performance
func BenchmarkLoadBalancerFactory(b *testing.B) {
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		lb := LoadBanlanceFactory(LbRoundRobin)
		lb.Add("127.0.0.1:8000")
	}
}

// Benchmark Update operations
func BenchmarkRoundRobinUpdate(b *testing.B) {
	rb := &RoundRobinBalance{}
	
	// Create mock config
	mockConf := &mockLoadBalanceConf{
		servers: []string{"127.0.0.1:8000,50", "127.0.0.1:8001,50"},
	}
	rb.SetConf(mockConf)
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		rb.Update()
	}
}

// Mock configuration for testing
type mockLoadBalanceConf struct {
	servers []string
}

func (m *mockLoadBalanceConf) GetConf() []string {
	return m.servers
}

func (m *mockLoadBalanceConf) Attach(o Observer) {}
func (m *mockLoadBalanceConf) WatchConf() {}
func (m *mockLoadBalanceConf) UpdateConf(conf []string) {
	m.servers = conf
}