package metrics

import (
	"sync"
	"sync/atomic"
	"time"
)

// Metrics collector for the gateway
type Metrics struct {
	// Request metrics
	TotalRequests     int64
	SuccessfulRequests int64
	FailedRequests    int64
	
	// Timing metrics
	AverageResponseTime time.Duration
	MinResponseTime     time.Duration
	MaxResponseTime     time.Duration
	
	// Load balancer metrics
	LBSelections map[string]int64
	LBErrors     int64
	
	// Connection pool metrics
	ActiveConnections int64
	PoolHits         int64
	PoolMisses       int64
	
	// Memory metrics
	AllocatedMemory int64
	GCCollections   int64
	
	mutex sync.RWMutex
	responseTimeSamples []time.Duration
	maxSamples int
}

// Global metrics instance
var globalMetrics = NewMetrics()

// NewMetrics creates a new metrics collector
func NewMetrics() *Metrics {
	return &Metrics{
		LBSelections: make(map[string]int64),
		maxSamples:   1000, // Keep last 1000 samples for calculating averages
		responseTimeSamples: make([]time.Duration, 0, 1000),
		MinResponseTime: time.Hour, // Start with a high value
	}
}

// GetGlobalMetrics returns the global metrics instance
func GetGlobalMetrics() *Metrics {
	return globalMetrics
}

// IncrementRequests atomically increments the total request counter
func (m *Metrics) IncrementRequests() {
	atomic.AddInt64(&m.TotalRequests, 1)
}

// IncrementSuccessfulRequests atomically increments successful request counter
func (m *Metrics) IncrementSuccessfulRequests() {
	atomic.AddInt64(&m.SuccessfulRequests, 1)
}

// IncrementFailedRequests atomically increments failed request counter
func (m *Metrics) IncrementFailedRequests() {
	atomic.AddInt64(&m.FailedRequests, 1)
}

// RecordResponseTime records a response time and updates statistics
func (m *Metrics) RecordResponseTime(duration time.Duration) {
	m.mutex.Lock()
	defer m.mutex.Unlock()
	
	// Update min/max
	if duration < m.MinResponseTime {
		m.MinResponseTime = duration
	}
	if duration > m.MaxResponseTime {
		m.MaxResponseTime = duration
	}
	
	// Add to samples (rolling window)
	if len(m.responseTimeSamples) >= m.maxSamples {
		// Remove oldest sample
		m.responseTimeSamples = m.responseTimeSamples[1:]
	}
	m.responseTimeSamples = append(m.responseTimeSamples, duration)
	
	// Calculate new average
	var total time.Duration
	for _, sample := range m.responseTimeSamples {
		total += sample
	}
	m.AverageResponseTime = total / time.Duration(len(m.responseTimeSamples))
}

// RecordLBSelection records a load balancer selection
func (m *Metrics) RecordLBSelection(backend string) {
	m.mutex.Lock()
	defer m.mutex.Unlock()
	m.LBSelections[backend]++
}

// IncrementLBErrors atomically increments load balancer error counter
func (m *Metrics) IncrementLBErrors() {
	atomic.AddInt64(&m.LBErrors, 1)
}

// UpdateActiveConnections updates the active connections counter
func (m *Metrics) UpdateActiveConnections(count int64) {
	atomic.StoreInt64(&m.ActiveConnections, count)
}

// IncrementPoolHits atomically increments connection pool hit counter
func (m *Metrics) IncrementPoolHits() {
	atomic.AddInt64(&m.PoolHits, 1)
}

// IncrementPoolMisses atomically increments connection pool miss counter
func (m *Metrics) IncrementPoolMisses() {
	atomic.AddInt64(&m.PoolMisses, 1)
}

// UpdateMemoryUsage updates memory usage metrics
func (m *Metrics) UpdateMemoryUsage(allocated int64) {
	atomic.StoreInt64(&m.AllocatedMemory, allocated)
}

// IncrementGCCollections atomically increments GC collection counter
func (m *Metrics) IncrementGCCollections() {
	atomic.AddInt64(&m.GCCollections, 1)
}

// GetSnapshot returns a snapshot of current metrics
func (m *Metrics) GetSnapshot() MetricsSnapshot {
	m.mutex.RLock()
	defer m.mutex.RUnlock()
	
	// Copy LB selections map
	lbSelectionsCopy := make(map[string]int64)
	for k, v := range m.LBSelections {
		lbSelectionsCopy[k] = v
	}
	
	return MetricsSnapshot{
		TotalRequests:       atomic.LoadInt64(&m.TotalRequests),
		SuccessfulRequests:  atomic.LoadInt64(&m.SuccessfulRequests),
		FailedRequests:      atomic.LoadInt64(&m.FailedRequests),
		AverageResponseTime: m.AverageResponseTime,
		MinResponseTime:     m.MinResponseTime,
		MaxResponseTime:     m.MaxResponseTime,
		LBSelections:        lbSelectionsCopy,
		LBErrors:            atomic.LoadInt64(&m.LBErrors),
		ActiveConnections:   atomic.LoadInt64(&m.ActiveConnections),
		PoolHits:            atomic.LoadInt64(&m.PoolHits),
		PoolMisses:          atomic.LoadInt64(&m.PoolMisses),
		AllocatedMemory:     atomic.LoadInt64(&m.AllocatedMemory),
		GCCollections:       atomic.LoadInt64(&m.GCCollections),
		Timestamp:           time.Now(),
	}
}

// MetricsSnapshot represents a point-in-time snapshot of metrics
type MetricsSnapshot struct {
	TotalRequests       int64
	SuccessfulRequests  int64
	FailedRequests      int64
	AverageResponseTime time.Duration
	MinResponseTime     time.Duration
	MaxResponseTime     time.Duration
	LBSelections        map[string]int64
	LBErrors            int64
	ActiveConnections   int64
	PoolHits            int64
	PoolMisses          int64
	AllocatedMemory     int64
	GCCollections       int64
	Timestamp           time.Time
}

// CalculateSuccessRate calculates the success rate as a percentage
func (s MetricsSnapshot) CalculateSuccessRate() float64 {
	if s.TotalRequests == 0 {
		return 0.0
	}
	return float64(s.SuccessfulRequests) / float64(s.TotalRequests) * 100.0
}

// CalculatePoolHitRate calculates the connection pool hit rate as a percentage
func (s MetricsSnapshot) CalculatePoolHitRate() float64 {
	total := s.PoolHits + s.PoolMisses
	if total == 0 {
		return 0.0
	}
	return float64(s.PoolHits) / float64(total) * 100.0
}

// Reset resets all metrics to zero
func (m *Metrics) Reset() {
	m.mutex.Lock()
	defer m.mutex.Unlock()
	
	atomic.StoreInt64(&m.TotalRequests, 0)
	atomic.StoreInt64(&m.SuccessfulRequests, 0)
	atomic.StoreInt64(&m.FailedRequests, 0)
	atomic.StoreInt64(&m.LBErrors, 0)
	atomic.StoreInt64(&m.ActiveConnections, 0)
	atomic.StoreInt64(&m.PoolHits, 0)
	atomic.StoreInt64(&m.PoolMisses, 0)
	atomic.StoreInt64(&m.AllocatedMemory, 0)
	atomic.StoreInt64(&m.GCCollections, 0)
	
	m.AverageResponseTime = 0
	m.MinResponseTime = time.Hour
	m.MaxResponseTime = 0
	m.LBSelections = make(map[string]int64)
	m.responseTimeSamples = m.responseTimeSamples[:0]
}