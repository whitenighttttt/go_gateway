#!/bin/bash

# Performance-optimized build script for GO_GATEWAY
# This script builds optimized binaries with reduced size and better performance

set -e

echo "Building optimized GO_GATEWAY binaries..."

# Build flags for optimization
BUILD_FLAGS="-ldflags=-s -w -X main.Version=$(git describe --tags --always --dirty 2>/dev/null || echo 'dev')"

# Build reverse proxy
echo "Building reverse proxy..."
go build $BUILD_FLAGS -o bin/reverse_proxy ./proxy/reverse_proxy_step

# Build load balancer demo
echo "Building load balancer demo..."
go build $BUILD_FLAGS -o bin/load_balancer_demo ./demo/proxy/load_balance

# Build simple proxy
echo "Building simple proxy..."
go build $BUILD_FLAGS -o bin/simple_proxy ./proxy

# Show binary sizes
echo ""
echo "Binary sizes:"
ls -lh bin/

# Run tests
echo ""
echo "Running tests..."
go test ./proxy/load_balance/...

echo "Build completed successfully!"