package main

import (
	"log"
	"net/http"
	"net/url"
	"net/http/httputil"
)

var addr = "127.0.0.1:2002"

func main(){
	rs1 := "http://127.0.0.1:2003/base"
	url1, err1 := url.Parse(rs1)
	if err1 != nil {
		log.Println(err1)
	}
	proxy := httputil.NewSingleHostReverseProxy(url1)
	log.Println("Starting httpserver at :2000")
	log.Fatal(http.ListenAndServe(":2000", proxy))
}