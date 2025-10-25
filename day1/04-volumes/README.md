# Day 1 - Docker Volumes

## The Problem: Data Persistence

By default, container data is lost when the container is removed. Volumes solve this problem by providing persistent storage.

## What are Docker Volumes?

Volumes are the preferred mechanism for persisting data generated and used by Docker containers.

### Benefits of Volumes:
- Data persists even after container removal
- Can be shared between containers
- Easier to back up and migrate
- Work on both Linux and Windows containers
- Can be managed using Docker CLI

## Types of Storage

### 1. Volumes (Recommended)
Managed by Docker, stored in Docker's storage directory.

### 2. Bind Mounts
Map a host directory to a container directory.

### 3. tmpfs Mounts
Stored in host memory only (Linux only).

```
┌─────────────────────────────────────────┐
│          Container                      │
│  ┌─────────────────────────────────┐   │
│  │  /app/data  (Volume)            │   │
│  │  /app/config (Bind Mount)       │   │
│  │  /tmp (tmpfs)                   │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
         │         │         │
         ▼         ▼         ▼
    Docker     Host      Host
    Volume     Dir       Memory
```

## Working with Volumes

### Create a Volume

```bash
docker volume create my-volume
```

### List Volumes

```bash
docker volume ls
```

### Inspect a Volume

```bash
docker volume inspect my-volume
```

### Remove a Volume

```bash
docker volume rm my-volume
docker volume prune  # Remove all unused volumes
```

## Exercise 1: Using Named Volumes

Run a container with a volume:
```bash
docker run -d --name mysql-db \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret123 \
  mysql:8
```

Create some data:
```bash
docker exec -it mysql-db mysql -uroot -psecret123 -e "CREATE DATABASE testdb;"
docker exec -it mysql-db mysql -uroot -psecret123 -e "SHOW DATABASES;"
```

Remove the container:
```bash
docker rm -f mysql-db
```

Start a new container with the same volume:
```bash
docker run -d --name mysql-db-new \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret123 \
  mysql:8
```

Verify data persists:
```bash
docker exec -it mysql-db-new mysql -uroot -psecret123 -e "SHOW DATABASES;"
```

## Exercise 2: Anonymous Volumes

Docker automatically creates anonymous volumes:
```bash
docker run -d --name nginx-temp -v /usr/share/nginx/html nginx
docker volume ls
```

These volumes are harder to manage and track.

## Bind Mounts

Bind mounts link a host directory to a container directory.

### Exercise 3: Using Bind Mounts

Create a local directory:
```bash
mkdir -p ~/docker-demo/html
echo "<h1>Hello from Bind Mount!</h1>" > ~/docker-demo/html/index.html
```

Run container with bind mount:
```bash
docker run -d --name web-bind \
  -p 8080:80 \
  -v ~/docker-demo/html:/usr/share/nginx/html:ro \
  nginx
```

Test it:
```bash
curl http://localhost:8080
```

Modify the file on host:
```bash
echo "<h1>Updated Content!</h1>" > ~/docker-demo/html/index.html
curl http://localhost:8080
```

The `:ro` flag makes the mount read-only in the container.

## Exercise 4: Development Environment

Create a Node.js project:

**app.js**
```javascript
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello from Express! Version 1.0');
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

**package.json**
```json
{
  "name": "docker-dev-demo",
  "version": "1.0.0",
  "main": "app.js",
  "dependencies": {
    "express": "^4.18.0"
  },
  "scripts": {
    "start": "node app.js"
  }
}
```

**Dockerfile**
```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

Build and run with bind mount for development:
```bash
docker build -t node-dev .
docker run -d --name dev-server \
  -p 3000:3000 \
  -v $(pwd):/app \
  -v /app/node_modules \
  node-dev
```

Now you can edit `app.js` on your host, and changes reflect in the container!

## Volume Drivers

Docker supports different volume drivers for various storage backends:
- local (default)
- nfs
- cifs
- AWS EBS
- Azure Disk
- GCP Persistent Disk

## Exercise 5: Sharing Volumes Between Containers

Start a data container:
```bash
docker run -d --name data-producer \
  -v shared-data:/data \
  busybox sh -c "while true; do echo $(date) >> /data/log.txt; sleep 5; done"
```

Start a consumer container:
```bash
docker run -d --name data-consumer \
  -v shared-data:/data \
  busybox sh -c "while true; do tail -n 5 /data/log.txt; sleep 10; done"
```

View the consumer logs:
```bash
docker logs -f data-consumer
```

## Backup and Restore

### Backup a Volume

```bash
docker run --rm \
  -v mysql-data:/data \
  -v $(pwd):/backup \
  ubuntu tar czf /backup/mysql-data-backup.tar.gz -C /data .
```

### Restore a Volume

```bash
docker run --rm \
  -v mysql-data:/data \
  -v $(pwd):/backup \
  ubuntu tar xzf /backup/mysql-data-backup.tar.gz -C /data
```

## Exercise 6: PostgreSQL with Persistent Data

Create a volume:
```bash
docker volume create postgres-data
```

Run PostgreSQL:
```bash
docker run -d --name postgres-db \
  -v postgres-data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=secret123 \
  -p 5432:5432 \
  postgres:15
```

Connect and create data:
```bash
docker exec -it postgres-db psql -U postgres -c "CREATE DATABASE myapp;"
docker exec -it postgres-db psql -U postgres -c "\l"
```

Test persistence:
```bash
docker rm -f postgres-db
docker run -d --name postgres-db-restored \
  -v postgres-data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=secret123 \
  -p 5432:5432 \
  postgres:15

# Wait a few seconds for startup
sleep 5
docker exec -it postgres-db-restored psql -U postgres -c "\l"
```

## Volume Location

Find where volumes are stored on the host:
```bash
docker volume inspect postgres-data
```

On Linux, typically: `/var/lib/docker/volumes/`

## tmpfs Mounts (Linux Only)

Store data in memory only:
```bash
docker run -d --name tmp-test \
  --tmpfs /app/temp:rw,size=100m \
  nginx
```

Data in `/app/temp` is stored in RAM and lost when container stops.

## Best Practices

1. **Use named volumes** for better management
2. **Backup important volumes** regularly
3. **Use bind mounts** for development only
4. **Read-only mounts** when data shouldn't be modified
5. **Clean up unused volumes** with `docker volume prune`
6. **Document volume requirements** in docker-compose or README
7. **Use volume drivers** for cloud storage when needed

## Volume vs Bind Mount Comparison

| Feature | Volume | Bind Mount |
|---------|--------|------------|
| Managed by Docker | ✓ | ✗ |
| Cross-platform | ✓ | Limited |
| Performance | Better | Good |
| Backup | Easier | Manual |
| Use case | Production | Development |

## Common Patterns

### Database Data
```bash
docker run -v db-data:/var/lib/mysql mysql
```

### Configuration Files
```bash
docker run -v ./config:/etc/app/config:ro app-image
```

### Logs
```bash
docker run -v log-data:/var/log app-image
```

### Application Code (Development)
```bash
docker run -v $(pwd):/app -v /app/node_modules app-image
```

## Quick Reference

```bash
# Create volume
docker volume create vol-name

# List volumes
docker volume ls

# Inspect volume
docker volume inspect vol-name

# Remove volume
docker volume rm vol-name

# Clean up unused volumes
docker volume prune

# Use volume in container
docker run -v vol-name:/path/in/container image

# Use bind mount
docker run -v /host/path:/container/path image

# Read-only mount
docker run -v vol-name:/path:ro image
```

## Next Steps

Continue to [Docker Networks](../05-networks/README.md) to learn about container networking.
