# Multi-stage build for optimized GO_GATEWAY
FROM golang:1.22-alpine AS builder

# Install build dependencies
RUN apk add --no-cache git ca-certificates tzdata

# Set working directory
WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build optimized binaries
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o reverse_proxy ./proxy/reverse_proxy_step && \
    CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o load_balancer_demo ./demo/proxy/load_balance && \
    CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o simple_proxy ./proxy

# Final stage
FROM alpine:latest

# Install runtime dependencies
RUN apk --no-cache add ca-certificates tzdata

# Create non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Set working directory
WORKDIR /app

# Copy binaries from builder stage
COPY --from=builder /app/reverse_proxy /app/load_balancer_demo /app/simple_proxy ./

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose ports
EXPOSE 2000 2002

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:2002/health || exit 1

# Default command
CMD ["./reverse_proxy"]