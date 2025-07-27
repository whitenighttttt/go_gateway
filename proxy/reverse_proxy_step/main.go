package main

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"regexp"
	"strings"
	"time"
)

var addr = "127.0.0.1:2002"

// Pre-compile regex for better performance
var pathRewriteRegex = regexp.MustCompile("^/dir(.*)")

func main() {
	//127.0.0.1:2002/xxx
	//127.0.0.1:2003/base/xxx
	rs1 := "http://127.0.0.1:2003/base"
	url1, err1 := url.Parse(rs1)
	if err1 != nil {
		log.Println(err1)
	}
	proxy := NewSingleHostReverseProxy(url1)
	
	// Configure server with proper timeouts
	server := &http.Server{
		Addr:           addr,
		Handler:        proxy,
		ReadTimeout:    30 * time.Second,
		WriteTimeout:   30 * time.Second,
		IdleTimeout:    120 * time.Second,
		MaxHeaderBytes: 1 << 20, // 1MB
	}
	
	log.Println("Starting httpserver at " + addr)
	log.Fatal(server.ListenAndServe())
}

func NewSingleHostReverseProxy(target *url.URL) *httputil.ReverseProxy {
	//http://127.0.0.1:2002/dir?name=123
	//RayQuery: name=123
	//Scheme: http
	//Host: 127.0.0.1:2002
	targetQuery := target.RawQuery
	director := func(req *http.Request) {
		//url_rewrite
		//127.0.0.1:2002/dir/abc ==> 127.0.0.1:2003/base/abc ??
		//127.0.0.1:2002/dir/abc ==> 127.0.0.1:2002/abc
		//127.0.0.1:2002/abc ==> 127.0.0.1:2003/base/abc
		req.URL.Path = pathRewriteRegex.ReplaceAllString(req.URL.Path, "$1")

		req.URL.Scheme = target.Scheme
		req.URL.Host = target.Host

		//target.Path : /base
		//req.URL.Path : /dir
		req.URL.Path = singleJoiningSlash(target.Path, req.URL.Path)
		if targetQuery == "" || req.URL.RawQuery == "" {
			req.URL.RawQuery = targetQuery + req.URL.RawQuery
		} else {
			req.URL.RawQuery = targetQuery + "&" + req.URL.RawQuery
		}
		if _, ok := req.Header["User-Agent"]; !ok {
			req.Header.Set("User-Agent", "")
		}
		
		// Add timeout context
		ctx, cancel := context.WithTimeout(req.Context(), 25*time.Second)
		*req = *req.WithContext(ctx)
		// Store cancel function for cleanup if needed
		req.Header.Set("X-Cancel-Func", fmt.Sprintf("%p", cancel))
	}
	
	modifyFunc := func(res *http.Response) error {
		if res.StatusCode != 200 {
			// Only read body for error responses, and limit size
			const maxErrorBodySize = 1024 * 1024 // 1MB limit
			
			if res.ContentLength > maxErrorBodySize {
				return errors.New("error response too large")
			}
			
			// Use LimitReader to prevent reading too much data
			limitedReader := io.LimitReader(res.Body, maxErrorBodySize)
			oldPayload, err := io.ReadAll(limitedReader)
			if err != nil {
				return fmt.Errorf("failed to read error response: %w", err)
			}
			
			newPayLoad := []byte("hello " + string(oldPayload))
			res.Body = io.NopCloser(bytes.NewBuffer(newPayLoad))
			res.ContentLength = int64(len(newPayLoad))
			res.Header.Set("Content-Length", fmt.Sprint(len(newPayLoad)))
		}
		return nil
	}
	
	errorHandler := func(res http.ResponseWriter, req *http.Request, err error) {
		// Clean up context cancel function if it exists
		if cancelStr := req.Header.Get("X-Cancel-Func"); cancelStr != "" {
			// The cancel function will be called automatically when the context times out
			req.Header.Del("X-Cancel-Func")
		}
		
		// Set proper error response headers
		res.Header().Set("Content-Type", "text/plain; charset=utf-8")
		res.WriteHeader(http.StatusBadGateway)
		
		// Write error message
		errorMsg := fmt.Sprintf("Proxy Error: %v", err)
		res.Write([]byte(errorMsg))
	}
	
	return &httputil.ReverseProxy{
		Director:       director,
		ModifyResponse: modifyFunc,
		ErrorHandler:   errorHandler,
	}
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