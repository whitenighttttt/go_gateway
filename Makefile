# Go Gateway Makefile - Performance Optimized

APP_NAME = go_gateway
VERSION := $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
BUILD_TIME := $(shell date -u '+%Y-%m-%d_%H:%M:%S')
COMMIT_HASH := $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")

# Build flags for optimization
LDFLAGS = -ldflags "-X main.Version=$(VERSION) -X main.BuildTime=$(BUILD_TIME) -X main.CommitHash=$(COMMIT_HASH) -s -w"
GCFLAGS = -gcflags="all=-trimpath=$(PWD)"
ASMFLAGS = -asmflags="all=-trimpath=$(PWD)"

# Build targets
.PHONY: all build build-optimized build-race test benchmark clean deps update

all: deps test benchmark build-optimized

# Regular build
build:
	go build -o bin/$(APP_NAME) ./proxy

# Optimized build for production
build-optimized:
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
		$(LDFLAGS) $(GCFLAGS) $(ASMFLAGS) \
		-a -installsuffix cgo \
		-o bin/$(APP_NAME)-optimized ./proxy

# Build with race detection for development
build-race:
	go build -race -o bin/$(APP_NAME)-race ./proxy

# Cross-compile for multiple platforms
build-all:
	GOOS=linux GOARCH=amd64 go build $(LDFLAGS) -o bin/$(APP_NAME)-linux-amd64 ./proxy
	GOOS=darwin GOARCH=amd64 go build $(LDFLAGS) -o bin/$(APP_NAME)-darwin-amd64 ./proxy
	GOOS=windows GOARCH=amd64 go build $(LDFLAGS) -o bin/$(APP_NAME)-windows-amd64.exe ./proxy

# Run tests
test:
	go test -v ./proxy/load_balance/...
	go test -v ./proxy/zookeeper/...

# Run tests with coverage
test-coverage:
	go test -coverprofile=coverage.out ./proxy/load_balance/...
	go tool cover -html=coverage.out -o coverage.html

# Run benchmarks
benchmark:
	go test -bench=. -benchmem -cpuprofile=cpu.prof -memprofile=mem.prof ./proxy/load_balance/
	go tool pprof -top cpu.prof
	go tool pprof -top mem.prof

# Run performance profiling
profile:
	go test -bench=BenchmarkRoundRobin -cpuprofile=cpu.prof ./proxy/load_balance/
	go tool pprof cpu.prof

# Memory profiling
memprofile:
	go test -bench=BenchmarkRoundRobinMemory -memprofile=mem.prof ./proxy/load_balance/
	go tool pprof mem.prof

# Install dependencies
deps:
	go mod download
	go mod verify

# Update dependencies
update:
	go get -u ./...
	go mod tidy

# Clean build artifacts
clean:
	rm -rf bin/
	rm -f *.prof *.out *.html

# Static analysis
lint:
	golangci-lint run ./...

# Security scan
security:
	gosec ./...

# Performance test with load
load-test:
	@echo "Starting load test..."
	ab -n 10000 -c 100 http://localhost:2000/

# Docker build optimized
docker-build:
	docker build -t $(APP_NAME):$(VERSION) -f Dockerfile.optimized .

# Generate performance report
perf-report:
	@echo "=== Performance Report ===" > performance-report.txt
	@echo "Build Version: $(VERSION)" >> performance-report.txt
	@echo "Build Time: $(BUILD_TIME)" >> performance-report.txt
	@echo "Commit: $(COMMIT_HASH)" >> performance-report.txt
	@echo "" >> performance-report.txt
	go test -bench=. -benchmem ./proxy/load_balance/ >> performance-report.txt

# Install build tools
install-tools:
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
	go install github.com/securecodewarrior/gosec/v2/cmd/gosec@latest

# Help
help:
	@echo "Available targets:"
	@echo "  build            - Regular build"
	@echo "  build-optimized  - Optimized production build"
	@echo "  build-race       - Build with race detection"
	@echo "  build-all        - Cross-compile for multiple platforms"
	@echo "  test             - Run tests"
	@echo "  test-coverage    - Run tests with coverage report"
	@echo "  benchmark        - Run performance benchmarks"
	@echo "  profile          - CPU profiling"
	@echo "  memprofile       - Memory profiling"
	@echo "  deps             - Install dependencies"
	@echo "  update           - Update dependencies"
	@echo "  clean            - Clean build artifacts"
	@echo "  lint             - Run static analysis"
	@echo "  security         - Run security scan"
	@echo "  load-test        - Run load test with Apache Bench"
	@echo "  perf-report      - Generate performance report"
	@echo "  install-tools    - Install development tools"