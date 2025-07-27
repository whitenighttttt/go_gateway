#!/bin/bash

# Performance benchmarking script for GO_GATEWAY
# This script tests the performance improvements

set -e

echo "Starting performance benchmarks..."

# Check if required tools are installed
command -v wrk >/dev/null 2>&1 || { echo "wrk is required but not installed. Install with: brew install wrk (macOS) or apt-get install wrk (Ubuntu)"; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "curl is required but not installed"; exit 1; }

# Build optimized version
echo "Building optimized version..."
go build -ldflags="-s -w" -o bin/reverse_proxy_optimized ./proxy/reverse_proxy_step

# Build unoptimized version for comparison
echo "Building unoptimized version..."
go build -o bin/reverse_proxy_unoptimized ./proxy/reverse_proxy_step

# Show binary sizes
echo ""
echo "Binary size comparison:"
echo "Optimized:   $(ls -lh bin/reverse_proxy_optimized | awk '{print $5}')"
echo "Unoptimized: $(ls -lh bin/reverse_proxy_unoptimized | awk '{print $5}')"

# Function to start proxy and run benchmarks
run_benchmark() {
    local binary=$1
    local name=$2
    
    echo ""
    echo "Testing $name..."
    
    # Start proxy in background
    ./$binary &
    local proxy_pid=$!
    
    # Wait for proxy to start
    sleep 2
    
    # Check if proxy is running
    if ! kill -0 $proxy_pid 2>/dev/null; then
        echo "Failed to start proxy"
        return 1
    fi
    
    # Run wrk benchmark
    echo "Running wrk benchmark..."
    wrk -t4 -c100 -d10s http://127.0.0.1:2002/ || true
    
    # Test response time
    echo "Testing response time..."
    time curl -s http://127.0.0.1:2002/ > /dev/null
    
    # Kill proxy
    kill $proxy_pid 2>/dev/null || true
    wait $proxy_pid 2>/dev/null || true
    
    echo "$name test completed"
}

# Create a simple test server
echo ""
echo "Starting test backend server..."
python3 -m http.server 2003 &
backend_pid=$!
sleep 1

# Run benchmarks
run_benchmark "bin/reverse_proxy_optimized" "Optimized Version"
run_benchmark "bin/reverse_proxy_unoptimized" "Unoptimized Version"

# Cleanup
kill $backend_pid 2>/dev/null || true
wait $backend_pid 2>/dev/null || true

echo ""
echo "Benchmark completed!"