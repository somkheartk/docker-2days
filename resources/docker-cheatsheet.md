# Docker Cheat Sheet

## Quick Reference Guide

### Container Basics

```bash
# Run container
docker run image                    # Run container from image
docker run -d image                # Run in detached mode
docker run -it image /bin/bash     # Interactive with terminal
docker run --name myapp image      # With custom name
docker run --rm image              # Remove after exit
docker run -p 8080:80 image        # Port mapping
docker run -v /host:/container image  # Volume mount
docker run -e KEY=value image      # Environment variable

# Container management
docker ps                          # List running containers
docker ps -a                       # List all containers
docker start container             # Start stopped container
docker stop container              # Stop running container
docker restart container           # Restart container
docker rm container                # Remove container
docker rm -f container             # Force remove running container
docker exec -it container bash     # Execute command in container
docker logs container              # View container logs
docker logs -f container           # Follow logs
docker inspect container           # Detailed info
docker stats container             # Resource usage
docker top container               # Process list
```

### Image Management

```bash
# Image operations
docker images                      # List local images
docker pull image                  # Download image
docker pull image:tag              # Download specific version
docker push image                  # Upload image to registry
docker build -t name:tag .         # Build image
docker build --no-cache -t name .  # Build without cache
docker rmi image                   # Remove image
docker tag source target           # Tag image
docker history image               # Show image layers
docker save -o file.tar image      # Save image to file
docker load -i file.tar            # Load image from file
docker search term                 # Search Docker Hub
docker image prune                 # Remove unused images
docker image prune -a              # Remove all unused images
```

### Dockerfile Instructions

```dockerfile
FROM image:tag              # Base image
LABEL key="value"          # Metadata
ENV KEY=value              # Environment variable
ARG KEY=value              # Build argument
WORKDIR /path              # Working directory
COPY src dest              # Copy files
ADD src dest               # Copy files (with extras)
RUN command                # Execute command
CMD ["executable"]         # Default command
ENTRYPOINT ["executable"]  # Container executable
EXPOSE port                # Document ports
VOLUME /path               # Create mount point
USER username              # Set user
HEALTHCHECK CMD command    # Health check
SHELL ["executable"]       # Set shell
```

### Docker Compose

```bash
# Basic commands
docker compose up                  # Start services
docker compose up -d              # Start in background
docker compose down               # Stop and remove
docker compose down -v            # Also remove volumes
docker compose start              # Start services
docker compose stop               # Stop services
docker compose restart            # Restart services
docker compose ps                 # List containers
docker compose logs               # View logs
docker compose logs -f            # Follow logs
docker compose logs service       # Service logs
docker compose exec service cmd   # Execute command
docker compose run service cmd    # Run one-off command
docker compose build              # Build images
docker compose build --no-cache   # Build without cache
docker compose pull               # Pull images
docker compose push               # Push images
docker compose config             # Validate and view config
docker compose top                # Display processes
```

### docker-compose.yml Structure

```yaml
version: '3.8'

services:
  service-name:
    image: image:tag
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - KEY=value
    container_name: custom-name
    command: ["executable", "arg"]
    entrypoint: ["executable"]
    environment:
      - KEY=value
      - KEY=${ENV_VAR}
    env_file:
      - .env
    ports:
      - "8080:80"
      - "443:443"
    expose:
      - "8080"
    volumes:
      - /host:/container
      - volume-name:/container
      - /container
    networks:
      - network-name
    depends_on:
      - other-service
    restart: always
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 40s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

volumes:
  volume-name:
    driver: local
    driver_opts:
      type: none
      device: /host/path
      o: bind

networks:
  network-name:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### Volume Management

```bash
# Volume operations
docker volume create volume        # Create volume
docker volume ls                   # List volumes
docker volume inspect volume       # Inspect volume
docker volume rm volume            # Remove volume
docker volume prune                # Remove unused volumes

# Using volumes
docker run -v volume:/path image   # Named volume
docker run -v /host:/container image  # Bind mount
docker run -v /container image     # Anonymous volume
docker run -v /path:ro image       # Read-only mount
```

### Network Management

```bash
# Network operations
docker network create network      # Create network
docker network ls                  # List networks
docker network inspect network     # Inspect network
docker network rm network          # Remove network
docker network prune               # Remove unused networks
docker network connect net cont    # Connect container
docker network disconnect net cont # Disconnect container

# Network drivers
--network bridge                   # Default bridge
--network host                     # Host network
--network none                     # No network
--network container:name           # Share network
--network custom-network           # Custom network
```

### System Management

```bash
# System info
docker version                     # Docker version
docker info                        # System information
docker system df                   # Disk usage
docker system df -v                # Verbose disk usage
docker system events               # Real-time events
docker system prune                # Remove unused data
docker system prune -a             # Remove all unused data
docker system prune --volumes      # Include volumes

# Clean up
docker container prune             # Remove stopped containers
docker image prune                 # Remove unused images
docker image prune -a              # Remove all unused images
docker volume prune                # Remove unused volumes
docker network prune               # Remove unused networks
```

### Registry Operations

```bash
# Registry commands
docker login                       # Login to registry
docker login registry.example.com  # Login to private registry
docker logout                      # Logout
docker pull image                  # Pull from registry
docker push image                  # Push to registry
docker tag local registry/image    # Tag for registry
docker search term                 # Search Docker Hub
```

### Debugging

```bash
# Logs and debugging
docker logs container              # Container logs
docker logs -f container           # Follow logs
docker logs --tail 100 container   # Last 100 lines
docker logs --since 30m container  # Last 30 minutes
docker exec -it container bash     # Interactive shell
docker inspect container           # Full details
docker inspect --format='{{.State}}' container  # Specific info
docker stats                       # Live resource stats
docker stats container             # Specific container stats
docker top container               # Process list
docker port container              # Port mappings
docker diff container              # File changes
docker events                      # System events
```

### Docker Build Arguments

```bash
# Build options
--build-arg KEY=value             # Build argument
--cache-from image                # Cache source
--file Dockerfile                 # Custom Dockerfile
--no-cache                        # Disable cache
--pull                            # Always pull base image
--quiet                           # Suppress output
--tag name:tag                    # Name and tag
--target stage                    # Multi-stage target
```

### Docker Run Options

```bash
# Common options
-d, --detach                      # Background
-i, --interactive                 # Keep STDIN open
-t, --tty                         # Allocate TTY
--rm                              # Remove on exit
--name string                     # Container name
-p, --publish list                # Publish ports
-P, --publish-all                 # Publish all ports
-v, --volume list                 # Bind mount
-e, --env list                    # Environment vars
--env-file list                   # Env file
--network string                  # Network
--restart policy                  # Restart policy
-w, --workdir string              # Working directory
--user string                     # Username or UID
-m, --memory bytes                # Memory limit
--cpus decimal                    # CPU limit
--privileged                      # Extended privileges
--read-only                       # Read-only filesystem
--health-cmd string               # Health check command
--health-interval duration        # Health check interval
```

### Useful Commands

```bash
# Copy files
docker cp container:/file /host   # From container
docker cp /host/file container:/  # To container

# Export/Import
docker export container > file.tar  # Export container
docker import file.tar image        # Import as image

# Save/Load
docker save image > file.tar      # Save image
docker load < file.tar            # Load image

# Commit container
docker commit container image     # Create image from container

# Resource limits
docker run -m 512m image          # Memory limit
docker run --cpus=2 image         # CPU limit
docker run --memory-swap 1g image # Swap limit
```

### Best Practices

```bash
# Image tagging
image:latest                      # Latest version
image:1.0                         # Major version
image:1.0.1                       # Specific version
image:sha256-abc123               # Digest

# Security
docker scan image                 # Scan for vulnerabilities
docker run --read-only image      # Read-only filesystem
docker run --cap-drop=ALL image   # Drop capabilities
docker run --user 1000:1000 image # Non-root user

# Cleanup
docker system prune -a --volumes  # Clean everything
docker container prune -f         # Force remove containers
docker image prune -a -f          # Force remove images
```

### Environment Variables

```bash
# Common Docker environment variables
DOCKER_HOST=unix:///var/run/docker.sock
DOCKER_TLS_VERIFY=1
DOCKER_CERT_PATH=/path/to/certs
DOCKER_CONFIG=/path/to/config
DOCKER_BUILDKIT=1                # Enable BuildKit
COMPOSE_PROJECT_NAME=myproject   # Compose project name
COMPOSE_FILE=docker-compose.yml  # Compose file path
```

### Restart Policies

```bash
--restart no                      # Never restart
--restart on-failure              # On non-zero exit
--restart on-failure:3            # Max 3 retries
--restart always                  # Always restart
--restart unless-stopped          # Unless manually stopped
```

### Health Check Example

```dockerfile
HEALTHCHECK --interval=30s \
            --timeout=3s \
            --start-period=5s \
            --retries=3 \
  CMD curl -f http://localhost/ || exit 1
```

### Quick Troubleshooting

```bash
# Container won't start
docker logs container
docker inspect container
docker run -it --entrypoint /bin/sh image

# Network issues
docker network inspect network
docker exec container ping other
docker exec container netstat -tlnp

# Permission issues
docker exec container ls -la /path
docker run -u $(id -u):$(id -g) image

# Resource issues
docker stats
docker system df
df -h
```

### Keyboard Shortcuts in Container

```bash
Ctrl+P, Ctrl+Q    # Detach from container (keep running)
Ctrl+D            # Exit container (stops it)
Ctrl+C            # Stop current process
```

### Tips

- Use `.dockerignore` to exclude files from build context
- Use multi-stage builds to reduce image size
- Always specify image tags (don't use `latest`)
- Run containers as non-root user
- Use health checks for production
- Set resource limits
- Use named volumes for data persistence
- Use networks for container isolation
- Clean up regularly with `docker system prune`
- Keep secrets out of images and compose files

## Common Patterns

### Web App with Database
```bash
docker network create app-net
docker run -d --name db --network app-net postgres
docker run -d --name web --network app-net -p 80:80 webapp
```

### Development with Hot Reload
```bash
docker run -it --rm -v $(pwd):/app -p 3000:3000 node npm run dev
```

### Backup Volume
```bash
docker run --rm -v vol:/data -v $(pwd):/backup ubuntu tar czf /backup/backup.tar.gz -C /data .
```

### Restore Volume
```bash
docker run --rm -v vol:/data -v $(pwd):/backup ubuntu tar xzf /backup/backup.tar.gz -C /data
```
