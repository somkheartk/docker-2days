# Day 2 - Dockerfile Best Practices

## Writing Efficient Dockerfiles

A well-written Dockerfile creates smaller, faster, and more secure images.

## Order Matters: Layer Caching

Docker caches each layer. Place instructions that change less frequently at the top.

### Bad Example
```dockerfile
FROM node:18
COPY . /app
WORKDIR /app
RUN npm install
CMD ["npm", "start"]
```

Every code change invalidates the cache and reinstalls dependencies!

### Good Example
```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
```

Now dependencies are only installed when `package.json` changes!

## Multi-Stage Builds

Reduce final image size by using multiple build stages.

### Example: Go Application

**Single Stage (Large)**
```dockerfile
FROM golang:1.21
WORKDIR /app
COPY . .
RUN go build -o myapp
CMD ["./myapp"]
```

Result: ~800MB image (includes entire Go toolchain)

**Multi-Stage (Small)**
```dockerfile
# Build stage
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Final stage
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/myapp .
CMD ["./myapp"]
```

Result: ~15MB image (only the binary)

## Exercise 1: Multi-Stage Node.js Build

**Dockerfile**
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Final stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["node", "app.js"]
```

## Minimize Layer Count

Each RUN, COPY, ADD creates a layer. Combine commands when possible.

### Bad
```dockerfile
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN apt-get clean
```

### Good
```dockerfile
RUN apt-get update && \
    apt-get install -y \
    curl \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

## Use Specific Base Image Tags

### Bad
```dockerfile
FROM node:latest
FROM ubuntu
FROM python
```

### Good
```dockerfile
FROM node:18.17-alpine
FROM ubuntu:22.04
FROM python:3.11-slim
```

Benefits:
- Reproducible builds
- Smaller images (alpine, slim variants)
- Security and stability

## Exercise 2: Optimize Python Application

**Before Optimization**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

**After Optimization**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Changes:
- Use slim variant (smaller base)
- Copy requirements first (better caching)
- Use `--no-cache-dir` (smaller image)

## Use .dockerignore

Create `.dockerignore` to exclude files from build context:

```
# .dockerignore
node_modules
npm-debug.log
.git
.gitignore
.env
*.md
.DS_Store
.vscode
*.pyc
__pycache__
.pytest_cache
dist
build
*.egg-info
```

Benefits:
- Faster builds
- Smaller build context
- Avoid copying sensitive files

## Don't Run as Root

### Bad
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "app.js"]
```

Runs as root (security risk)

### Good
```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

CMD ["node", "app.js"]
```

## Use COPY Instead of ADD

- `COPY` is more explicit and preferred
- `ADD` has extra features (auto-extract tar, URL support) that can be confusing

### Use COPY
```dockerfile
COPY package.json /app/
COPY . /app/
```

### Only use ADD when you need its features
```dockerfile
ADD https://example.com/file.tar.gz /tmp/
```

## Leverage Build Cache

### Example: Python Dependencies

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first (cached unless requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code (changes frequently)
COPY . .

CMD ["python", "app.py"]
```

## Exercise 3: Complete Optimized Dockerfile

**Node.js Production Ready**

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Production stage
FROM node:18-alpine
WORKDIR /app

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create non-root user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

# Copy dependencies from builder
COPY --from=builder --chown=appuser:appuser /app/node_modules ./node_modules

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 3000

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start application
CMD ["node", "app.js"]
```

## ARG vs ENV

**ARG**: Build-time variables
```dockerfile
ARG NODE_VERSION=18
FROM node:${NODE_VERSION}
```

**ENV**: Runtime environment variables
```dockerfile
ENV NODE_ENV=production
ENV PORT=3000
```

## Use LABEL for Metadata

```dockerfile
LABEL maintainer="your-email@example.com"
LABEL version="1.0"
LABEL description="My awesome application"
```

## Health Checks

Add health checks for production:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

## Exercise 4: Complete Production Dockerfile

**app.py**
```python
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify(message="Hello from Flask!")

@app.route('/health')
def health():
    return jsonify(status="healthy")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**requirements.txt**
```
Flask==2.3.0
gunicorn==21.2.0
```

**Dockerfile**
```dockerfile
# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install curl for health checks
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Update PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD curl -f http://localhost:5000/health || exit 1

# Start application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

**.dockerignore**
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.git
.gitignore
.dockerignore
README.md
```

Build and test:
```bash
docker build -t flask-prod .
docker run -d -p 5000:5000 --name flask-app flask-prod
curl http://localhost:5000
docker inspect --format='{{.State.Health.Status}}' flask-app
```

## Security Best Practices

### 1. Use Official Base Images
```dockerfile
FROM node:18-alpine  # Official Node.js image
```

### 2. Keep Base Images Updated
```bash
docker pull node:18-alpine
docker build -t myapp .
```

### 3. Scan Images for Vulnerabilities
```bash
docker scan myapp
```

### 4. Don't Store Secrets
Never put passwords, keys, or tokens in Dockerfiles!

### Bad
```dockerfile
ENV DATABASE_PASSWORD=secret123
```

### Good
```bash
docker run -e DATABASE_PASSWORD=secret123 myapp
```

### 5. Use Read-Only Root Filesystem
```bash
docker run --read-only myapp
```

## Image Size Optimization

### Comparison of Base Images

| Base Image | Size |
|------------|------|
| ubuntu:22.04 | 77MB |
| python:3.11 | 1GB |
| python:3.11-slim | 130MB |
| python:3.11-alpine | 50MB |
| alpine:latest | 7MB |

### Tips for Smaller Images

1. Use Alpine or slim variants
2. Multi-stage builds
3. Remove package manager caches
4. Combine RUN commands
5. Remove unnecessary files

## Exercise 5: Extreme Optimization

**Scratch Image (Smallest Possible)**

For compiled languages like Go:

```dockerfile
# Build stage
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

# Final stage
FROM scratch
COPY --from=builder /app/app /app
EXPOSE 8080
CMD ["/app"]
```

Result: Only the binary, ~5-10MB!

## Best Practices Checklist

- [ ] Use specific image tags
- [ ] Use multi-stage builds
- [ ] Optimize layer caching
- [ ] Use .dockerignore
- [ ] Run as non-root user
- [ ] Add health checks
- [ ] Minimize layers
- [ ] Remove unnecessary files
- [ ] Use COPY over ADD
- [ ] Document with LABEL
- [ ] Set proper working directory
- [ ] Use alpine or slim variants
- [ ] Don't store secrets

## Quick Reference

```dockerfile
# Good Dockerfile template
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine
WORKDIR /app
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser
COPY --from=builder --chown=appuser:appuser /app/node_modules ./node_modules
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 3000
HEALTHCHECK CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
CMD ["node", "app.js"]
```

## Next Steps

Continue to [Docker Compose](../02-docker-compose/README.md) to learn about multi-container applications.
