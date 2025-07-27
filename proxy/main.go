package main

import (
	"GO_GATEWAY/proxy/load_balance"
	"context"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"sync"
	"time"
)

var (
	addr = "127.0.0.1:2002"
	
	// HTTP client pool for better performance
	httpClientPool = &sync.Pool{
		New: func() interface{} {
			return &http.Client{
				Transport: &http.Transport{
					MaxIdleConns:        100,
					MaxIdleConnsPerHost: 10,
					IdleConnTimeout:     90 * time.Second,
					DisableCompression:  false,
				},
				Timeout: 30 * time.Second,
			}
		},
	}
	
	// Load balancer instance
	loadBalancer load_balance.LoadBalance
)

func init() {
	// Initialize load balancer with some default servers
	loadBalancer = load_balance.LoadBanlanceFactory(load_balance.LbRoundRobin)
	loadBalancer.Add("http://127.0.0.1:2003/base")
	loadBalancer.Add("http://127.0.0.1:2004/base")
}

func main() {
	// Create optimized reverse proxy
	proxy := NewOptimizedReverseProxy()
	
	// Configure server with proper settings
	server := &http.Server{
		Addr:           ":2000",
		Handler:        proxy,
		ReadTimeout:    30 * time.Second,
		WriteTimeout:   30 * time.Second,
		IdleTimeout:    120 * time.Second,
		MaxHeaderBytes: 1 << 20, // 1MB
	}
	
	log.Println("Starting optimized httpserver at :2000")
	log.Fatal(server.ListenAndServe())
}

func NewOptimizedReverseProxy() *httputil.ReverseProxy {
	director := func(req *http.Request) {
		// Get target from load balancer
		target, err := loadBalancer.Get(req.RemoteAddr)
		if err != nil || target == "" {
			log.Printf("Load balancer error: %v", err)
			target = "http://127.0.0.1:2003/base" // fallback
		}
		
		targetURL, err := url.Parse(target)
		if err != nil {
			log.Printf("Invalid target URL: %v", err)
			return
		}
		
		req.URL.Scheme = targetURL.Scheme
		req.URL.Host = targetURL.Host
		req.URL.Path = singleJoiningSlash(targetURL.Path, req.URL.Path)
		
		if targetURL.RawQuery == "" || req.URL.RawQuery == "" {
			req.URL.RawQuery = targetURL.RawQuery + req.URL.RawQuery
		} else {
			req.URL.RawQuery = targetURL.RawQuery + "&" + req.URL.RawQuery
		}
		
		if _, ok := req.Header["User-Agent"]; !ok {
			req.Header.Set("User-Agent", "")
		}
		
		// Add request timeout
		ctx, cancel := context.WithTimeout(req.Context(), 25*time.Second)
		*req = *req.WithContext(ctx)
		req.Header.Set("X-Cancel-Func", "set") // Mark for cleanup
		_ = cancel // Will be called when context times out
	}
	
	// Use custom transport with connection pooling
	transport := &http.Transport{
		MaxIdleConns:        100,
		MaxIdleConnsPerHost: 10,
		IdleConnTimeout:     90 * time.Second,
		DisableCompression:  false,
		ResponseHeaderTimeout: 30 * time.Second,
	}
	
	return &httputil.ReverseProxy{
		Director:  director,
		Transport: transport,
		ErrorHandler: func(w http.ResponseWriter, r *http.Request, err error) {
			log.Printf("Proxy error: %v", err)
			w.WriteHeader(http.StatusBadGateway)
			w.Write([]byte("Gateway Error"))
		},
	}
}

func singleJoiningSlash(a, b string) string {
	if a == "" {
		return b
	}
	if b == "" {
		return a
	}
	
	aslash := a[len(a)-1] == '/'
	bslash := b[0] == '/'
	
	switch {
	case aslash && bslash:
		return a + b[1:]
	case !aslash && !bslash:
		return a + "/" + b
	}
	return a + b
}