# Day 1 - Docker Containers

## What is a Docker Container?

A container is a runnable instance of an image. It's an isolated process running on the host machine, sharing the OS kernel with other containers.

## Container Lifecycle

```
Create → Start → Running → Stop → Remove
```

## Running Containers

### Basic Run Command

```bash
docker run nginx
```

This will:
1. Pull the image if not available locally
2. Create a container
3. Start the container
4. Attach to container output

### Detached Mode

Run container in background:
```bash
docker run -d nginx
docker run -d --name my-nginx nginx
```

### Interactive Mode

Run with terminal access:
```bash
docker run -it ubuntu bash
docker run -it --name my-ubuntu ubuntu bash
```

### Port Mapping

Map container port to host port:
```bash
docker run -d -p 8080:80 nginx
docker run -d -p 127.0.0.1:8080:80 nginx  # Bind to specific IP
```

Multiple port mappings:
```bash
docker run -d -p 8080:80 -p 8443:443 nginx
```

## Exercise 1: Run Web Server

Run an Nginx server:
```bash
docker run -d --name web-server -p 8080:80 nginx
```

Test it:
```bash
curl http://localhost:8080
```

Access logs:
```bash
docker logs web-server
docker logs -f web-server  # Follow logs
```

Stop the container:
```bash
docker stop web-server
```

Start it again:
```bash
docker start web-server
```

## Managing Containers

### List Containers

Running containers:
```bash
docker ps
```

All containers:
```bash
docker ps -a
```

Container IDs only:
```bash
docker ps -q
```

### Stop Containers

```bash
docker stop container-name
docker stop container-id
docker stop $(docker ps -q)  # Stop all running containers
```

### Remove Containers

```bash
docker rm container-name
docker rm -f container-name  # Force remove (even if running)
docker rm $(docker ps -aq)   # Remove all stopped containers
```

### Container Cleanup

Remove stopped containers:
```bash
docker container prune
```

Remove container automatically after exit:
```bash
docker run --rm ubuntu echo "Hello World"
```

## Exercise 2: Container States

Create a container without starting:
```bash
docker create --name test-container nginx
docker ps -a
```

Start the container:
```bash
docker start test-container
docker ps
```

Pause the container:
```bash
docker pause test-container
docker ps
```

Unpause the container:
```bash
docker unpause test-container
```

Restart the container:
```bash
docker restart test-container
```

## Executing Commands in Containers

Run command in running container:
```bash
docker exec container-name command
```

Interactive shell:
```bash
docker exec -it container-name bash
docker exec -it container-name sh  # For Alpine-based images
```

### Exercise 3: Working Inside Containers

Start a container:
```bash
docker run -d --name ubuntu-test ubuntu sleep 3600
```

Execute commands:
```bash
docker exec ubuntu-test ls /
docker exec ubuntu-test cat /etc/os-release
```

Open interactive shell:
```bash
docker exec -it ubuntu-test bash
```

Inside the container:
```bash
apt-get update
apt-get install -y curl
curl --version
exit
```

## Container Logs

View logs:
```bash
docker logs container-name
docker logs -f container-name          # Follow logs
docker logs --tail 50 container-name   # Last 50 lines
docker logs --since 30m container-name # Last 30 minutes
docker logs -t container-name          # Show timestamps
```

## Container Inspection

Get detailed information:
```bash
docker inspect container-name
docker inspect --format='{{.State.Status}}' container-name
docker inspect --format='{{.NetworkSettings.IPAddress}}' container-name
```

## Container Statistics

Real-time resource usage:
```bash
docker stats
docker stats container-name
docker top container-name  # Process list
```

## Exercise 4: Environment Variables

Run container with environment variables:
```bash
docker run -d --name mysql-db \
  -e MYSQL_ROOT_PASSWORD=secret123 \
  -e MYSQL_DATABASE=myapp \
  -e MYSQL_USER=appuser \
  -e MYSQL_PASSWORD=apppass \
  mysql:8
```

Check environment variables:
```bash
docker exec mysql-db env
```

## Exercise 5: Complete Web Application

**app.py**
```python
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    name = os.environ.get('APP_NAME', 'Docker App')
    return f'Hello from {name}!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**requirements.txt**
```
Flask==2.3.0
```

**Dockerfile**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t flask-app .
docker run -d --name my-flask-app -p 5000:5000 -e APP_NAME="My Awesome App" flask-app
curl http://localhost:5000
```

## Container Naming

Good naming practices:
```bash
docker run -d --name web-server-prod nginx
docker run -d --name web-server-dev nginx
docker run -d --name api-backend-v1 node:18
```

## Resource Limits

Limit CPU and memory:
```bash
docker run -d --name limited-nginx \
  --memory="256m" \
  --cpus="0.5" \
  nginx
```

Check resource limits:
```bash
docker inspect limited-nginx | grep -A 10 "Memory"
```

## Container Restart Policies

```bash
docker run -d --restart=no nginx           # Never restart
docker run -d --restart=on-failure nginx   # Restart on failure
docker run -d --restart=always nginx       # Always restart
docker run -d --restart=unless-stopped nginx  # Restart unless manually stopped
```

## Exercise 6: Debugging Containers

Start a container with issues:
```bash
docker run -d --name broken-app nginx
docker exec broken-app rm /usr/share/nginx/html/index.html
```

Debug:
```bash
docker logs broken-app
docker exec -it broken-app bash
# Find and fix the issue
```

## Container Health Checks

**Dockerfile with health check:**
```dockerfile
FROM nginx:alpine
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1
```

Check health status:
```bash
docker ps  # Shows health status
docker inspect --format='{{.State.Health.Status}}' container-name
```

## Best Practices

1. Use meaningful container names
2. Always use `-d` for production services
3. Implement proper logging
4. Set resource limits
5. Use restart policies
6. Clean up stopped containers regularly
7. Don't run containers as root (when possible)
8. Use health checks for production

## Quick Reference

```bash
# Run
docker run -d -p 8080:80 --name web nginx

# Manage
docker ps                    # List running
docker ps -a                 # List all
docker stop web             # Stop
docker start web            # Start
docker restart web          # Restart
docker rm web               # Remove

# Interact
docker logs web             # View logs
docker exec -it web bash    # Shell access
docker inspect web          # Detailed info
docker stats web            # Resource usage

# Cleanup
docker container prune      # Remove stopped containers
docker system prune         # Remove unused data
```

## Next Steps

Continue to [Docker Volumes](../04-volumes/README.md) to learn about data persistence.
