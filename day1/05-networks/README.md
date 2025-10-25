# Day 1 - Docker Networks

## Container Networking Basics

Docker networking allows containers to communicate with each other and the outside world.

## Network Drivers

Docker provides several network drivers:

1. **bridge** (default) - Isolated network on a single host
2. **host** - Remove network isolation, use host's network
3. **none** - Disable all networking
4. **overlay** - Connect multiple Docker daemons (Swarm)
5. **macvlan** - Assign MAC address to container

## Default Networks

List existing networks:
```bash
docker network ls
```

You'll see:
- `bridge` - Default network for containers
- `host` - Host machine's network
- `none` - No network access

## Bridge Network (Default)

When you run a container without specifying a network, it uses the default bridge network.

```bash
docker run -d --name web1 nginx
docker run -d --name web2 nginx
```

Containers on the same bridge network can communicate.

## Exercise 1: Inspect Default Bridge

Check the bridge network:
```bash
docker network inspect bridge
```

This shows:
- Network configuration
- Connected containers
- IP addresses

## User-Defined Bridge Networks

User-defined bridges are better than the default bridge because:
- Automatic DNS resolution between containers
- Better isolation
- Can connect/disconnect containers on the fly
- Better control over network settings

### Create a Custom Network

```bash
docker network create my-network
docker network ls
```

### Run Containers on Custom Network

```bash
docker run -d --name web --network my-network nginx
docker run -d --name api --network my-network node:18
```

## Exercise 2: Container Communication

Create a network:
```bash
docker network create app-network
```

Run a database:
```bash
docker run -d --name postgres \
  --network app-network \
  -e POSTGRES_PASSWORD=secret123 \
  postgres:15
```

Run an application that connects to the database:
```bash
docker run -d --name app \
  --network app-network \
  busybox sleep 3600
```

Test connectivity using container name:
```bash
docker exec app ping -c 3 postgres
```

The container name `postgres` automatically resolves to the container's IP!

## Exercise 3: Web Application with Database

Create network:
```bash
docker network create wordpress-net
```

Run MySQL:
```bash
docker run -d --name mysql \
  --network wordpress-net \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=wordpress \
  -e MYSQL_USER=wpuser \
  -e MYSQL_PASSWORD=wppass \
  mysql:8
```

Run WordPress:
```bash
docker run -d --name wordpress \
  --network wordpress-net \
  -p 8080:80 \
  -e WORDPRESS_DB_HOST=mysql \
  -e WORDPRESS_DB_USER=wpuser \
  -e WORDPRESS_DB_PASSWORD=wppass \
  -e WORDPRESS_DB_NAME=wordpress \
  wordpress:latest
```

Access WordPress at http://localhost:8080

## Network Commands

### Inspect a Network

```bash
docker network inspect my-network
```

### Connect Container to Network

```bash
docker network connect my-network container-name
```

### Disconnect Container from Network

```bash
docker network disconnect my-network container-name
```

### Remove a Network

```bash
docker network rm my-network
docker network prune  # Remove unused networks
```

## Exercise 4: Multiple Networks

Create two networks:
```bash
docker network create frontend
docker network create backend
```

Run database (backend only):
```bash
docker run -d --name db \
  --network backend \
  postgres:15 \
  -e POSTGRES_PASSWORD=secret
```

Run API (both networks):
```bash
docker run -d --name api \
  --network backend \
  nginx
docker network connect frontend api
```

Run web (frontend only):
```bash
docker run -d --name web \
  --network frontend \
  nginx
```

Now:
- `web` can reach `api` (both on frontend)
- `api` can reach `db` (both on backend)
- `web` cannot reach `db` (different networks)

## Host Network

Remove network isolation, use host's network directly:

```bash
docker run -d --name web-host --network host nginx
```

The container uses the host's networking stack. Access it on the host's IP address.

**Note**: Port mapping is not needed (and ignored) with host networking.

## None Network

Disable networking completely:

```bash
docker run -d --name isolated --network none nginx
```

The container has no network access.

## Port Mapping Review

Expose container ports to host:

```bash
# Map container port 80 to host port 8080
docker run -d -p 8080:80 nginx

# Map to specific host IP
docker run -d -p 127.0.0.1:8080:80 nginx

# Map to random host port
docker run -d -p 80 nginx
```

Find the mapped port:
```bash
docker port container-name
```

## Exercise 5: Multi-Tier Application

Create networks:
```bash
docker network create frontend-net
docker network create backend-net
```

Database tier:
```bash
docker run -d --name postgres \
  --network backend-net \
  -e POSTGRES_PASSWORD=secret123 \
  -e POSTGRES_DB=appdb \
  postgres:15
```

API tier (connects to both networks):
```bash
docker run -d --name api \
  --network backend-net \
  -e DATABASE_URL=postgresql://postgres:secret123@postgres:5432/appdb \
  nginx

docker network connect frontend-net api
```

Web tier:
```bash
docker run -d --name web \
  --network frontend-net \
  -p 8080:80 \
  nginx
```

## DNS Resolution

Containers on the same user-defined network can resolve each other by name:

```bash
docker network create test-net
docker run -d --name server1 --network test-net nginx
docker run -d --name server2 --network test-net nginx

docker exec server1 ping -c 2 server2
docker exec server2 ping -c 2 server1
```

## Network Aliases

Give containers additional DNS names:

```bash
docker network create app-net

docker run -d --name db1 \
  --network app-net \
  --network-alias database \
  postgres:15

docker run -d --name db2 \
  --network app-net \
  --network-alias database \
  postgres:15
```

Both containers respond to `database`:
```bash
docker run --rm --network app-net alpine ping -c 2 database
```

## Exercise 6: Load Balancing with Network Alias

Create network:
```bash
docker network create lb-net
```

Run multiple web servers with the same alias:
```bash
docker run -d --name web1 \
  --network lb-net \
  --network-alias webserver \
  -e MESSAGE="Server 1" \
  nginx

docker run -d --name web2 \
  --network lb-net \
  --network-alias webserver \
  -e MESSAGE="Server 2" \
  nginx

docker run -d --name web3 \
  --network lb-net \
  --network-alias webserver \
  -e MESSAGE="Server 3" \
  nginx
```

Test DNS round-robin:
```bash
docker run --rm --network lb-net alpine nslookup webserver
```

## Container Communication Patterns

### 1. Same Network
```
Container A ← → Container B
  (same network)
```

### 2. Different Networks
```
Container A ← → Container B (bridge network)
              ↓
         Container C (custom network)
```

### 3. Multi-Network
```
Frontend Net: Web ← → API
Backend Net:        API ← → DB
```

## Exposing Ports

In Dockerfile:
```dockerfile
EXPOSE 80 443
```

`EXPOSE` is documentation only. To actually publish ports, use `-p`:

```bash
docker run -p 8080:80 my-image
```

## Network Security

### Isolation
Different networks provide isolation:
```bash
docker network create public
docker network create private

# Public services
docker run --network public web-app

# Private services (no external access)
docker run --network private database
```

### Encrypted Networks
Overlay networks in Swarm mode can be encrypted:
```bash
docker network create --driver overlay --opt encrypted my-overlay
```

## Troubleshooting

### Check Container Network Settings

```bash
docker inspect container-name
docker inspect --format='{{.NetworkSettings.IPAddress}}' container-name
docker inspect --format='{{json .NetworkSettings.Networks}}' container-name
```

### Test Connectivity

```bash
# From host to container
curl http://localhost:8080

# From container to container
docker exec container1 ping container2
docker exec container1 wget -O- http://container2

# Check DNS resolution
docker exec container1 nslookup container2
```

### View Network Details

```bash
docker network inspect network-name
```

## Best Practices

1. **Use user-defined bridge networks** instead of default bridge
2. **Create separate networks** for different tiers (frontend, backend)
3. **Use container names** for communication (DNS)
4. **Don't expose unnecessary ports** to the host
5. **Use network aliases** for service discovery
6. **Clean up unused networks** regularly
7. **Document network requirements** in docker-compose files

## Quick Reference

```bash
# Create network
docker network create net-name

# List networks
docker network ls

# Inspect network
docker network inspect net-name

# Run container on network
docker run --network net-name image

# Connect running container
docker network connect net-name container

# Disconnect container
docker network disconnect net-name container

# Remove network
docker network rm net-name

# Clean up unused networks
docker network prune

# Port mapping
docker run -p host-port:container-port image
```

## Common Network Patterns

### Web + Database
```bash
docker network create app-net
docker run -d --name db --network app-net postgres
docker run -d --name web --network app-net -p 80:80 webapp
```

### Microservices
```bash
docker network create services
docker run -d --name api1 --network services api-image
docker run -d --name api2 --network services api-image
docker run -d --name gateway --network services -p 80:80 gateway-image
```

### Development Environment
```bash
docker network create dev-net
docker run -d --name redis --network dev-net redis
docker run -d --name postgres --network dev-net postgres
docker run -d --name app --network dev-net -p 3000:3000 -v $(pwd):/app app-image
```

## Day 1 Complete!

You've learned:
- ✓ Docker introduction and concepts
- ✓ Working with images
- ✓ Managing containers
- ✓ Data persistence with volumes
- ✓ Container networking

Continue to [Day 2](../../day2/01-dockerfile-best-practices/README.md) for advanced Docker topics!
