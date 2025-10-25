# Day 2 - Docker Best Practices

## Production-Ready Checklist

Use this checklist to ensure your Docker setup is production-ready.

## Security Best Practices

### 1. Never Run as Root

**Bad:**
```dockerfile
FROM node:18
COPY . /app
CMD ["node", "app.js"]
```

**Good:**
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser
CMD ["node", "app.js"]
```

### 2. Use Official Images

```dockerfile
# Good - Official images
FROM node:18-alpine
FROM python:3.11-slim
FROM postgres:15
FROM nginx:alpine

# Avoid - Unverified images
FROM random-user/node
FROM unofficial/python
```

### 3. Scan Images for Vulnerabilities

```bash
# Use Docker Scout or Trivy
docker scout cves myapp:latest
docker scan myapp:latest

# Use Trivy
trivy image myapp:latest
```

### 4. Don't Store Secrets in Images

**Bad:**
```dockerfile
ENV DATABASE_PASSWORD=secret123
ENV API_KEY=abcd1234
```

**Good:**
```bash
# Pass at runtime
docker run -e DATABASE_PASSWORD=$DB_PASS myapp

# Use Docker secrets
docker secret create db_password password.txt
docker service create --secret db_password myapp
```

### 5. Use Read-Only Filesystems

```bash
docker run --read-only myapp

# Or in docker-compose
services:
  app:
    image: myapp
    read_only: true
    tmpfs:
      - /tmp
```

### 6. Limit Container Capabilities

```bash
# Drop all capabilities and add only what's needed
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp

# In docker-compose
services:
  app:
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### 7. Use Security Profiles

```bash
# AppArmor
docker run --security-opt apparmor=docker-default myapp

# Seccomp
docker run --security-opt seccomp=/path/to/profile.json myapp
```

## Image Optimization

### 1. Use Multi-Stage Builds

```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

### 2. Minimize Layers

**Bad:**
```dockerfile
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN rm -rf /var/lib/apt/lists/*
```

**Good:**
```dockerfile
RUN apt-get update && \
    apt-get install -y curl vim && \
    rm -rf /var/lib/apt/lists/*
```

### 3. Order Dockerfile Commands Correctly

```dockerfile
FROM python:3.11-slim

# 1. Install system dependencies (changes rarely)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# 2. Set working directory
WORKDIR /app

# 3. Copy and install dependencies (changes occasionally)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy application code (changes frequently)
COPY . .

# 5. Set runtime configuration
EXPOSE 8000
CMD ["python", "app.py"]
```

### 4. Use .dockerignore

```
# .dockerignore
**/.git
**/.gitignore
**/.vscode
**/.idea
**/node_modules
**/dist
**/build
**/.env
**/.env.*
**/coverage
**/*.log
**/*.md
!README.md
**/Dockerfile
**/docker-compose*.yml
**/.dockerignore
```

### 5. Choose the Right Base Image

```dockerfile
# From largest to smallest
FROM ubuntu:22.04      # ~77MB
FROM python:3.11       # ~1GB
FROM python:3.11-slim  # ~130MB
FROM python:3.11-alpine # ~50MB
FROM alpine:latest     # ~7MB
FROM scratch           # 0MB (empty)
```

## Resource Management

### 1. Set Resource Limits

```yaml
services:
  app:
    image: myapp
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### 2. Use Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 5s
```

### 3. Set Restart Policies

```yaml
services:
  app:
    restart: unless-stopped  # or always, on-failure, no
```

### 4. Configure Logging

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Networking Best Practices

### 1. Use User-Defined Networks

```yaml
services:
  frontend:
    networks:
      - frontend-net
  
  api:
    networks:
      - frontend-net
      - backend-net
  
  database:
    networks:
      - backend-net

networks:
  frontend-net:
  backend-net:
```

### 2. Don't Expose Unnecessary Ports

```yaml
services:
  database:
    image: postgres
    # Don't expose database to host in production
    # expose: ["5432"]  # Only for inter-container communication
    networks:
      - backend
```

### 3. Use Network Aliases

```yaml
services:
  api:
    networks:
      backend:
        aliases:
          - api-service
          - backend-api
```

## Data Persistence

### 1. Use Named Volumes

**Good:**
```yaml
services:
  database:
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

**Avoid:**
```yaml
services:
  database:
    volumes:
      - /var/lib/postgresql/data  # Anonymous volume
```

### 2. Backup Volumes Regularly

```bash
# Backup
docker run --rm \
  -v db-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/db-backup-$(date +%Y%m%d).tar.gz -C /data .

# Restore
docker run --rm \
  -v db-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/db-backup-20240101.tar.gz -C /data
```

### 3. Use Bind Mounts for Configuration Only

```yaml
services:
  nginx:
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro  # Read-only config
      - nginx-logs:/var/log/nginx              # Named volume for logs
```

## Environment Configuration

### 1. Use .env Files

**.env** (Don't commit!)
```bash
DB_PASSWORD=secret123
API_KEY=abcd1234
JWT_SECRET=xyz789
```

**.env.example** (Commit this!)
```bash
DB_PASSWORD=changeme
API_KEY=changeme
JWT_SECRET=changeme
```

**docker-compose.yml**
```yaml
services:
  app:
    env_file:
      - .env
    environment:
      NODE_ENV: production
```

### 2. Validate Environment Variables

```bash
# In entrypoint script
#!/bin/sh
if [ -z "$DATABASE_URL" ]; then
  echo "ERROR: DATABASE_URL is not set"
  exit 1
fi
exec "$@"
```

## Monitoring and Logging

### 1. Structured Logging

```javascript
// Use structured logging
const logger = require('pino')();

logger.info({ user: 'john', action: 'login' }, 'User logged in');

// Instead of
console.log('User john logged in');
```

### 2. Export Metrics

```dockerfile
# Expose Prometheus metrics
EXPOSE 8000 9090
```

```javascript
const prometheus = require('prom-client');
const register = prometheus.register;

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

### 3. Implement Distributed Tracing

```yaml
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # UI
      - "6831:6831/udp"  # Agent
```

## CI/CD Integration

### 1. Build in CI

**.gitlab-ci.yml**
```yaml
build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

### 2. Run Tests in Containers

```yaml
test:
  stage: test
  script:
    - docker compose -f docker-compose.test.yml run --rm test
```

### 3. Security Scanning

```yaml
security:
  stage: test
  script:
    - trivy image $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

## Development vs Production

### Development (docker-compose.yml)
```yaml
version: '3.8'
services:
  app:
    build: .
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=*
    ports:
      - "3000:3000"
    command: npm run dev
```

### Production (docker-compose.prod.yml)
```yaml
version: '3.8'
services:
  app:
    image: registry.company.com/app:${VERSION}
    restart: always
    environment:
      - NODE_ENV=production
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
```

## Cleanup and Maintenance

### 1. Regular Cleanup

```bash
# Remove unused containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Remove everything unused
docker system prune -a --volumes
```

### 2. Set Up Automated Cleanup

```bash
# Cron job for daily cleanup
0 2 * * * docker system prune -f
```

### 3. Monitor Disk Usage

```bash
docker system df
docker system df -v
```

## Documentation

### 1. Document in README

```markdown
# MyApp

## Quick Start

```bash
docker compose up -d
```

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string (required)
- `REDIS_URL` - Redis connection string (required)
- `SECRET_KEY` - JWT secret (required)
- `DEBUG` - Enable debug mode (optional, default: false)

## Health Check

http://localhost:3000/health
```

### 2. Comment Complex Configurations

```yaml
services:
  app:
    # Use custom network for isolation
    networks:
      - backend
    
    # Mount config as read-only for security
    volumes:
      - ./config.yml:/app/config.yml:ro
    
    # Wait for database to be healthy before starting
    depends_on:
      db:
        condition: service_healthy
```

## Testing

### 1. Test Dockerfile Builds

```bash
docker build -t myapp:test .
docker run --rm myapp:test npm test
```

### 2. Integration Tests

**docker-compose.test.yml**
```yaml
version: '3.8'
services:
  test:
    build: .
    command: npm test
    depends_on:
      - db
      - redis
    environment:
      - NODE_ENV=test
      - DATABASE_URL=postgresql://test:test@db:5432/test
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: test
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
  
  redis:
    image: redis:alpine
```

Run tests:
```bash
docker compose -f docker-compose.test.yml run --rm test
docker compose -f docker-compose.test.yml down -v
```

## Production Checklist

- [ ] Images use specific tags, not `latest`
- [ ] Services run as non-root user
- [ ] Images are scanned for vulnerabilities
- [ ] Secrets are not in images or compose files
- [ ] Health checks are configured
- [ ] Resource limits are set
- [ ] Restart policies are configured
- [ ] Logging is properly configured
- [ ] Networks are segmented appropriately
- [ ] Volumes are used for persistent data
- [ ] Backups are configured
- [ ] Monitoring is in place
- [ ] Documentation is complete
- [ ] .dockerignore is optimized
- [ ] Multi-stage builds are used
- [ ] Images are optimized for size

## Common Mistakes to Avoid

1. **Running as root** - Security risk
2. **Using `latest` tag** - Unpredictable builds
3. **Storing secrets in images** - Security risk
4. **No health checks** - Can't detect failures
5. **No resource limits** - Can exhaust host resources
6. **Exposing unnecessary ports** - Attack surface
7. **Not using .dockerignore** - Slow builds, large images
8. **Poor layer ordering** - Slow builds
9. **Not cleaning up** - Disk space issues
10. **Missing documentation** - Hard to maintain

## Performance Tips

1. Use multi-stage builds
2. Optimize layer caching
3. Use alpine or slim variants
4. Remove package manager caches
5. Use specific COPY instead of COPY .
6. Combine RUN commands
7. Use .dockerignore
8. Leverage build cache
9. Use docker buildkit
10. Optimize for production

## Quick Commands Reference

```bash
# Build
docker build -t app:v1 .
docker compose build

# Run
docker run -d -p 8080:80 app:v1
docker compose up -d

# Logs
docker logs -f container
docker compose logs -f service

# Clean
docker system prune -a
docker volume prune

# Inspect
docker inspect container
docker compose ps

# Health
docker inspect --format='{{.State.Health.Status}}' container

# Resources
docker stats
docker system df
```

## Next Steps

Continue to [Troubleshooting](../05-troubleshooting/README.md) for debugging tips.
