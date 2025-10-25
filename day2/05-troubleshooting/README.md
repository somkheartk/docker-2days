# Day 2 - Troubleshooting Docker

## Common Issues and Solutions

This guide covers common Docker problems and how to solve them.

## Container Won't Start

### Problem: Container exits immediately

**Check logs:**
```bash
docker logs container-name
docker logs --tail 50 container-name
```

**Common causes:**
1. Application error in startup
2. Missing environment variables
3. Port already in use
4. Volume permission issues

**Solutions:**

Check last exit code:
```bash
docker inspect --format='{{.State.ExitCode}}' container-name
```

Run interactively to debug:
```bash
docker run -it image-name /bin/sh
```

Override entrypoint:
```bash
docker run -it --entrypoint /bin/sh image-name
```

## Network Issues

### Problem: Container can't connect to other containers

**Debug steps:**

1. Check if containers are on the same network:
```bash
docker network inspect network-name
```

2. Test DNS resolution:
```bash
docker exec container1 ping container2
docker exec container1 nslookup container2
```

3. Check if service is listening:
```bash
docker exec container netstat -tlnp
docker exec container ss -tlnp
```

4. Test connection:
```bash
docker exec container1 curl http://container2:port
docker exec container1 wget -O- http://container2:port
```

**Solutions:**

Ensure containers are on same network:
```yaml
services:
  app:
    networks:
      - mynetwork
  db:
    networks:
      - mynetwork

networks:
  mynetwork:
```

Use container names for DNS:
```bash
# Good
curl http://api-service:3000

# Bad
curl http://172.17.0.3:3000
```

### Problem: Can't access container from host

**Check port mapping:**
```bash
docker port container-name
docker ps  # Shows port mappings
```

**Verify service is listening:**
```bash
docker exec container netstat -tlnp
```

**Check firewall:**
```bash
sudo ufw status
sudo iptables -L
```

**Solution:**

Map ports correctly:
```bash
docker run -p 8080:80 image  # host:container
```

Bind to all interfaces:
```python
# Instead of
app.run(host='127.0.0.1', port=5000)

# Use
app.run(host='0.0.0.0', port=5000)
```

## Volume and Permission Issues

### Problem: Permission denied in container

**Check file ownership:**
```bash
docker exec container ls -la /path/to/files
```

**Solutions:**

1. Run container as specific user:
```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

2. Fix permissions in entrypoint:
```bash
#!/bin/sh
chown -R appuser:appuser /app/data
exec su-exec appuser "$@"
```

3. Match host user ID:
```bash
docker run -u $(id -u):$(id -g) image
```

### Problem: Data not persisting

**Check volume configuration:**
```bash
docker volume ls
docker volume inspect volume-name
docker inspect --format='{{.Mounts}}' container-name
```

**Solution:**

Use named volumes:
```yaml
services:
  db:
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

## Image Issues

### Problem: Image build fails

**Common errors:**

1. **COPY failed: no such file or directory**
   ```dockerfile
   # Check your context
   docker build -t myapp .
   
   # List build context
   docker build --no-cache -t myapp . 2>&1 | grep "COPY"
   ```

2. **RUN command fails**
   ```dockerfile
   # Add debugging
   RUN set -x && \
       apt-get update && \
       apt-get install -y package
   ```

3. **Dependency installation fails**
   ```dockerfile
   # Clear cache and retry
   RUN npm cache clean --force && npm install
   RUN pip install --no-cache-dir -r requirements.txt
   ```

**Solutions:**

Build without cache:
```bash
docker build --no-cache -t myapp .
```

Use build arguments for debugging:
```dockerfile
ARG DEBUG=false
RUN if [ "$DEBUG" = "true" ]; then set -x; fi && \
    apt-get update
```

Check .dockerignore:
```bash
cat .dockerignore
```

### Problem: Image too large

**Check image size:**
```bash
docker images
docker history image-name
```

**Solutions:**

1. Use multi-stage builds
2. Use alpine or slim variants
3. Clean up in same layer:
```dockerfile
RUN apt-get update && \
    apt-get install -y package && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

4. Remove build dependencies:
```dockerfile
RUN apk add --no-cache --virtual .build-deps gcc && \
    pip install package && \
    apk del .build-deps
```

## Performance Issues

### Problem: Slow container startup

**Debug:**
```bash
docker logs --timestamps container-name
time docker run image-name
```

**Solutions:**

1. Use health checks with start period:
```dockerfile
HEALTHCHECK --start-period=30s --interval=10s \
  CMD curl -f http://localhost/health || exit 1
```

2. Optimize dependencies installation
3. Use layer caching effectively

### Problem: High CPU/Memory usage

**Monitor resources:**
```bash
docker stats
docker stats --no-stream
docker top container-name
```

**Check specific container:**
```bash
docker stats container-name
```

**Solutions:**

Set resource limits:
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

Or with docker run:
```bash
docker run -m 512m --cpus=0.5 image
```

Find memory leaks:
```bash
docker exec container ps aux
docker exec container top
```

## Docker Compose Issues

### Problem: Service dependencies not working

**Issue:** Services start before dependencies are ready

**Solution:**

Use health checks:
```yaml
services:
  db:
    image: postgres
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
  
  app:
    depends_on:
      db:
        condition: service_healthy
```

Use wait scripts:
```dockerfile
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

CMD /wait && python app.py
```

### Problem: Environment variables not loading

**Debug:**
```bash
docker compose config  # View resolved config
docker compose exec service env  # Check variables
```

**Solutions:**

Check .env file location (must be in same directory as docker-compose.yml):
```bash
ls -la .env
```

Explicitly specify env_file:
```yaml
services:
  app:
    env_file:
      - .env
```

Use correct syntax:
```yaml
# Good
environment:
  - KEY=value
  - DATABASE_URL=${DATABASE_URL}

# Bad
environment:
  KEY: value  # YAML syntax, but can have issues
```

### Problem: Volumes not updating

**Issue:** Changes to bind-mounted files not reflected

**Solutions:**

1. Check mount path:
```bash
docker inspect --format='{{.Mounts}}' container
```

2. Restart container:
```bash
docker compose restart service
```

3. Force recreate:
```bash
docker compose up -d --force-recreate
```

4. On Mac/Windows, check Docker Desktop settings for file sharing

## Debugging Techniques

### 1. Interactive Debugging

Start with shell:
```bash
docker run -it --entrypoint /bin/sh image-name
```

Attach to running container:
```bash
docker exec -it container-name /bin/sh
```

### 2. Inspect Container State

Full inspection:
```bash
docker inspect container-name
```

Specific information:
```bash
docker inspect --format='{{.State.Status}}' container
docker inspect --format='{{.Config.Env}}' container
docker inspect --format='{{json .NetworkSettings}}' container | jq
```

### 3. View Logs

Real-time logs:
```bash
docker logs -f container-name
docker compose logs -f service-name
```

Last N lines:
```bash
docker logs --tail 100 container-name
```

With timestamps:
```bash
docker logs -t container-name
```

Since specific time:
```bash
docker logs --since 2024-01-01T10:00:00 container-name
docker logs --since 30m container-name
```

### 4. Network Debugging

Install debugging tools:
```bash
docker run -it --network container:container-name nicolaka/netshoot
```

Available tools: curl, wget, nslookup, dig, netstat, tcpdump, etc.

Test connectivity:
```bash
# From host
curl http://localhost:8080

# From container
docker exec container curl http://other-container:port

# Using netshoot
docker run --rm --network mynet nicolaka/netshoot curl http://service:port
```

### 5. Process Debugging

View processes:
```bash
docker top container-name
docker exec container ps aux
```

Check specific process:
```bash
docker exec container pidof app-name
docker exec container kill -SIGUSR1 <pid>
```

### 6. File System Debugging

Check file system:
```bash
docker exec container df -h
docker exec container ls -la /path
docker exec container cat /path/to/file
```

Copy files for analysis:
```bash
docker cp container:/path/to/file ./local-file
docker cp ./local-file container:/path/to/file
```

## Advanced Troubleshooting

### Enable Debug Mode

Docker daemon debug:
```json
{
  "debug": true,
  "log-level": "debug"
}
```

Restart Docker:
```bash
sudo systemctl restart docker
```

### Check Docker Daemon

Status:
```bash
sudo systemctl status docker
journalctl -u docker
```

Docker info:
```bash
docker info
docker version
```

### Network Packet Analysis

Capture packets:
```bash
docker run --rm --net=host --privileged \
  nicolaka/netshoot tcpdump -i any port 8080
```

### Container Events

Monitor events:
```bash
docker events
docker events --filter 'container=mycontainer'
docker events --filter 'type=network'
```

### System Resources

Check disk usage:
```bash
docker system df
docker system df -v
```

Check for resource exhaustion:
```bash
df -h
docker info | grep -i "Docker Root Dir"
```

## Common Error Messages

### "no space left on device"

**Solutions:**
```bash
# Clean up
docker system prune -a
docker volume prune

# Check disk space
df -h

# Change Docker data directory
# Edit /etc/docker/daemon.json
{
  "data-root": "/new/path"
}
```

### "port is already allocated"

**Solutions:**
```bash
# Find process using port
sudo lsof -i :8080
sudo netstat -tlnp | grep 8080

# Kill process
sudo kill <pid>

# Or use different port
docker run -p 8081:80 image
```

### "Cannot connect to Docker daemon"

**Solutions:**
```bash
# Check if Docker is running
sudo systemctl status docker

# Start Docker
sudo systemctl start docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Check socket permissions
ls -la /var/run/docker.sock
```

### "pull access denied"

**Solutions:**
```bash
# Login to registry
docker login

# Check image name
docker pull namespace/image:tag

# Check permissions
docker logout
docker login -u username
```

## Recovery Procedures

### Lost Container Data

Backup before removing:
```bash
docker commit container-name backup-image
docker export container-name > container-backup.tar
```

Restore from backup:
```bash
docker import container-backup.tar restored-image
```

### Corrupted Images

Remove and rebuild:
```bash
docker rmi -f image-name
docker system prune -a
docker build --no-cache -t image-name .
```

### Network Issues After System Restart

Reset networks:
```bash
docker network prune
docker compose down
docker compose up -d
```

## Preventive Measures

1. **Use health checks** to detect failures early
2. **Set up monitoring** (Prometheus, Grafana)
3. **Configure logging** properly
4. **Regular backups** of volumes
5. **Test deployments** in staging first
6. **Document** known issues and solutions
7. **Version control** docker-compose files
8. **Use restart policies** for resilience

## Diagnostic Script

```bash
#!/bin/bash
# docker-diagnostic.sh

echo "=== Docker Version ==="
docker version

echo "\n=== Docker Info ==="
docker info

echo "\n=== Running Containers ==="
docker ps

echo "\n=== Container Logs (last 20 lines) ==="
for container in $(docker ps -q); do
  echo "--- $container ---"
  docker logs --tail 20 $container
done

echo "\n=== Resource Usage ==="
docker stats --no-stream

echo "\n=== Disk Usage ==="
docker system df

echo "\n=== Network List ==="
docker network ls

echo "\n=== Volume List ==="
docker volume ls

echo "\n=== Recent Events ==="
docker events --since 1h --until 0s
```

## Getting Help

1. Check logs first: `docker logs container`
2. Search Docker documentation: https://docs.docker.com
3. Search Docker forums: https://forums.docker.com
4. Stack Overflow: tag `docker`
5. GitHub issues for specific images
6. Docker community Slack

## Quick Troubleshooting Checklist

- [ ] Check container logs
- [ ] Verify container is running
- [ ] Check port mappings
- [ ] Verify network connectivity
- [ ] Check volume mounts
- [ ] Verify environment variables
- [ ] Check resource usage
- [ ] Review recent changes
- [ ] Test with minimal configuration
- [ ] Check Docker daemon logs

## Course Complete!

Congratulations! You've completed the Docker 2-Day Training Course. You now know:

- ✓ Docker fundamentals and architecture
- ✓ Working with images and containers
- ✓ Data persistence with volumes
- ✓ Container networking
- ✓ Dockerfile best practices
- ✓ Docker Compose for multi-container apps
- ✓ Real-world application patterns
- ✓ Production best practices
- ✓ Troubleshooting techniques

## Next Steps

- Practice building your own applications
- Explore Docker Swarm or Kubernetes
- Learn about container orchestration
- Study security hardening
- Implement CI/CD with Docker
- Contribute to Docker community

Happy Dockering! 🐳
