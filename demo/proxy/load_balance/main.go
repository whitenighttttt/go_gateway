package main

import (
	"GO_GATEWAY/proxy/load_balance"
	"bytes"
	"io"
	"log"
	"net"
	"net/http"
	"net/http/httputil"
	"net/url"
	"strconv"
	"strings"
	"sync"
	"time"
)

var (
	addr = "127.0.0.1:2002"
	// Optimized transport configuration for better performance
	transport = &http.Transport{
		DialContext: (&net.Dialer{
			Timeout:   10 * time.Second,  // Reduced from 30s for faster failure detection
			KeepAlive: 30 * time.Second,  // Keep-alive timeout
			DualStack: true,              // Enable IPv4/IPv6 dual-stack
		}).DialContext,
		MaxIdleConns:          200,              // Increased from 100 for better connection reuse
		MaxIdleConnsPerHost:   10,               // Limit connections per host
		IdleConnTimeout:       90 * time.Second, // Idle connection timeout
		TLSHandshakeTimeout:   5 * time.Second,  // Reduced from 10s
		ExpectContinueTimeout: 1 * time.Second,  // 100-continue timeout
		DisableCompression:    true,             // Disable compression for proxy
		ForceAttemptHTTP2:     true,             // Enable HTTP/2
	}
	
	// Buffer pool for reducing memory allocations
	bufferPool = sync.Pool{
		New: func() interface{} {
			return new(bytes.Buffer)
		},
	}
)

func NewMultipleHostsReverseProxy(lb load_balance.LoadBalance) *httputil.ReverseProxy {
	//请求协调者
	director := func(req *http.Request) {
		nextAddr, err := lb.Get(req.RemoteAddr)
		if err != nil {
			log.Printf("get next addr fail: %v", err)
			return
		}
		target, err := url.Parse(nextAddr)
		if err != nil {
			log.Printf("parse target url fail: %v", err)
			return
		}
		targetQuery := target.RawQuery
		req.URL.Scheme = target.Scheme
		req.URL.Host = target.Host
		req.URL.Path = singleJoiningSlash(target.Path, req.URL.Path)
		if targetQuery == "" || req.URL.RawQuery == "" {
			req.URL.RawQuery = targetQuery + req.URL.RawQuery
		} else {
			req.URL.RawQuery = targetQuery + "&" + req.URL.RawQuery
		}
		if _, ok := req.Header["User-Agent"]; !ok {
			req.Header.Set("User-Agent", "user-agent")
		}
	}

	//更改内容
	modifyFunc := func(resp *http.Response) error {
		//请求以下命令：curl 'http://127.0.0.1:2002/error'
		if resp.StatusCode != 200 {
			// Use buffer pool to reduce memory allocations
			buf := bufferPool.Get().(*bytes.Buffer)
			buf.Reset()
			defer bufferPool.Put(buf)
			
			//获取内容
			oldPayload, err := io.ReadAll(resp.Body)
			if err != nil {
				return err
			}
			resp.Body.Close()
			
			// Pre-allocate buffer with exact size needed
			prefix := "StatusCode error:"
			newPayload := make([]byte, len(prefix)+len(oldPayload))
			copy(newPayload, prefix)
			copy(newPayload[len(prefix):], oldPayload)
			
			resp.Body = io.NopCloser(bytes.NewReader(newPayload))
			resp.ContentLength = int64(len(newPayload))
			resp.Header.Set("Content-Length", strconv.FormatInt(int64(len(newPayload)), 10))
		}
		return nil
	}

	//错误回调 ：关闭real_server时测试，错误回调
	//范围：transport.RoundTrip发生的错误、以及ModifyResponse发生的错误
	errFunc := func(w http.ResponseWriter, r *http.Request, err error) {
		//todo 如果是权重的负载则调整临时权重
		log.Printf("Error handling request: %v", err)
		http.Error(w, "ErrorHandler error:"+err.Error(), 500)
	}

	return &httputil.ReverseProxy{Director: director, Transport: transport, ModifyResponse: modifyFunc, ErrorHandler: errFunc}
}

func singleJoiningSlash(a, b string) string {
	aslash := strings.HasSuffix(a, "/")
	bslash := strings.HasPrefix(b, "/")
	switch {
	case aslash && bslash:
		return a + b[1:]
	case !aslash && !bslash:
		return a + "/" + b
	}
	return a + b
}

func main() {
	rb := load_balance.LoadBanlanceFactory(load_balance.LbWeightRoundRobin)
	if err := rb.Add("http://127.0.0.1:2003/base", "10"); err != nil {
		log.Println(err)
	}
	if err := rb.Add("http://127.0.0.1:2004/base", "20"); err != nil {
		log.Println(err)
	}
	proxy := NewMultipleHostsReverseProxy(rb)
	log.Println("Starting httpserver at " + addr)
	log.Fatal(http.ListenAndServe(addr, proxy))
}