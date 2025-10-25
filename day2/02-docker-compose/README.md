# Day 2 - Docker Compose

## What is Docker Compose?

Docker Compose is a tool for defining and running multi-container Docker applications using a YAML file.

### Benefits:
- Define entire application stack in one file
- Start all services with one command
- Easy to share and version control
- Consistent development environments
- Service dependencies and ordering

## Installing Docker Compose

Docker Compose is included with Docker Desktop. For Linux:

```bash
docker compose version
```

## Basic docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

Start the application:
```bash
docker compose up
```

Stop the application:
```bash
docker compose down
```

## Exercise 1: Simple Web Application

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
```

Create `html/index.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Docker Compose Demo</title>
</head>
<body>
    <h1>Hello from Docker Compose!</h1>
</body>
</html>
```

Run:
```bash
docker compose up -d
curl http://localhost:8080
docker compose logs
docker compose down
```

## Service Configuration Options

### Common Options

```yaml
services:
  app:
    image: myapp:latest           # Use existing image
    build: .                       # Build from Dockerfile
    container_name: my-app         # Custom container name
    ports:
      - "8080:80"                  # Port mapping
    volumes:
      - ./data:/app/data           # Volume mount
    environment:
      - NODE_ENV=production        # Environment variables
    depends_on:
      - database                   # Start after database
    restart: always                # Restart policy
    networks:
      - frontend                   # Custom network
```

## Exercise 2: Web App with Database

```yaml
version: '3.8'

services:
  database:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: secret123
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - backend

  web:
    image: nginx
    ports:
      - "8080:80"
    depends_on:
      - database
    networks:
      - frontend
      - backend

volumes:
  postgres-data:

networks:
  frontend:
  backend:
```

## Building Images with Compose

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - NODE_VERSION=18
    image: myapp:latest
    ports:
      - "3000:3000"
```

Build and run:
```bash
docker compose build
docker compose up -d
```

Rebuild without cache:
```bash
docker compose build --no-cache
```

## Exercise 3: Node.js App with Redis

**app.js**
```javascript
const express = require('express');
const redis = require('redis');

const app = express();
const client = redis.createClient({
  host: 'redis',
  port: 6379
});

app.get('/', async (req, res) => {
  const visits = await client.incr('visits');
  res.send(`Number of visits: ${visits}`);
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

**package.json**
```json
{
  "name": "redis-demo",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.0",
    "redis": "^4.6.0"
  }
}
```

**Dockerfile**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["node", "app.js"]
```

**docker-compose.yml**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - redis
    environment:
      - NODE_ENV=production
    volumes:
      - .:/app
      - /app/node_modules

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

Run:
```bash
docker compose up --build
# Visit http://localhost:3000 multiple times
```

## Environment Variables

### Method 1: Define in compose file
```yaml
services:
  app:
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/myapp
      - DEBUG=true
```

### Method 2: Use .env file

**.env**
```
DATABASE_URL=postgres://user:pass@db:5432/myapp
DEBUG=true
SECRET_KEY=my-secret-key
```

**docker-compose.yml**
```yaml
services:
  app:
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - DEBUG=${DEBUG}
      - SECRET_KEY=${SECRET_KEY}
```

### Method 3: env_file
```yaml
services:
  app:
    env_file:
      - .env
      - .env.production
```

## Exercise 4: WordPress with MySQL

**docker-compose.yml**
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wpuser
      MYSQL_PASSWORD: wppass
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - wordpress-net

  wordpress:
    image: wordpress:latest
    depends_on:
      - mysql
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: mysql:3306
      WORDPRESS_DB_USER: wpuser
      WORDPRESS_DB_PASSWORD: wppass
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wordpress-data:/var/www/html
    networks:
      - wordpress-net

volumes:
  mysql-data:
  wordpress-data:

networks:
  wordpress-net:
```

Start:
```bash
docker compose up -d
```

Access http://localhost:8080 and complete WordPress setup.

## Docker Compose Commands

### Start services
```bash
docker compose up                # Foreground
docker compose up -d             # Background (detached)
docker compose up --build        # Rebuild images
```

### Stop services
```bash
docker compose stop              # Stop containers
docker compose down              # Stop and remove containers
docker compose down -v           # Also remove volumes
```

### View status
```bash
docker compose ps                # List containers
docker compose logs              # View logs
docker compose logs -f           # Follow logs
docker compose logs web          # Logs for specific service
```

### Execute commands
```bash
docker compose exec web bash     # Shell in running container
docker compose run web bash      # Run new container
```

### Scale services
```bash
docker compose up -d --scale web=3
```

### Other useful commands
```bash
docker compose build             # Build images
docker compose pull              # Pull images
docker compose restart           # Restart services
docker compose pause             # Pause services
docker compose unpause           # Unpause services
```

## Exercise 5: Microservices Application

**docker-compose.yml**
```yaml
version: '3.8'

services:
  # Frontend
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - api
    networks:
      - frontend-net

  # API Gateway
  api:
    build: ./api
    ports:
      - "4000:4000"
    depends_on:
      - users-service
      - products-service
    networks:
      - frontend-net
      - backend-net
    environment:
      - USERS_SERVICE=http://users-service:5001
      - PRODUCTS_SERVICE=http://products-service:5002

  # Users Microservice
  users-service:
    build: ./services/users
    expose:
      - "5001"
    depends_on:
      - users-db
    networks:
      - backend-net
    environment:
      - DATABASE_URL=postgres://user:pass@users-db:5432/users

  # Products Microservice
  products-service:
    build: ./services/products
    expose:
      - "5002"
    depends_on:
      - products-db
    networks:
      - backend-net
    environment:
      - DATABASE_URL=postgres://user:pass@products-db:5432/products

  # Databases
  users-db:
    image: postgres:15
    environment:
      POSTGRES_DB: users
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - users-data:/var/lib/postgresql/data
    networks:
      - backend-net

  products-db:
    image: postgres:15
    environment:
      POSTGRES_DB: products
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - products-data:/var/lib/postgresql/data
    networks:
      - backend-net

volumes:
  users-data:
  products-data:

networks:
  frontend-net:
  backend-net:
```

## Depends On and Health Checks

Wait for service to be healthy:

```yaml
version: '3.8'

services:
  database:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    build: .
    depends_on:
      database:
        condition: service_healthy
```

## Override Files

**docker-compose.yml** (base)
```yaml
version: '3.8'
services:
  app:
    image: myapp
    environment:
      - NODE_ENV=production
```

**docker-compose.override.yml** (development)
```yaml
version: '3.8'
services:
  app:
    volumes:
      - .:/app
    environment:
      - NODE_ENV=development
      - DEBUG=true
```

By default, both files are used. For production:
```bash
docker compose -f docker-compose.yml up
```

For development (default):
```bash
docker compose up
```

## Exercise 6: Development vs Production

**docker-compose.yml**
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
```

**docker-compose.dev.yml**
```yaml
version: '3.8'

services:
  app:
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=*
    command: npm run dev
```

Run development:
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## Real-World Stack Example

**docker-compose.yml**
```yaml
version: '3.8'

services:
  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    networks:
      - frontend

  # Web Application
  web:
    build: ./app
    expose:
      - "3000"
    depends_on:
      - database
      - redis
      - rabbitmq
    environment:
      - DATABASE_URL=postgres://user:pass@database:5432/myapp
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
    networks:
      - frontend
      - backend
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure

  # PostgreSQL Database
  database:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - backend

  # Redis Cache
  redis:
    image: redis:alpine
    networks:
      - backend
    volumes:
      - redis-data:/data

  # RabbitMQ Message Queue
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "15672:15672"  # Management UI
    networks:
      - backend
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq

  # Worker
  worker:
    build: ./app
    command: python worker.py
    depends_on:
      - database
      - rabbitmq
    environment:
      - DATABASE_URL=postgres://user:pass@database:5432/myapp
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
    networks:
      - backend
    deploy:
      replicas: 2

volumes:
  postgres-data:
  redis-data:
  rabbitmq-data:

networks:
  frontend:
  backend:
```

## Best Practices

1. **Use version control** for compose files
2. **Use .env files** for secrets (add to .gitignore)
3. **Use named volumes** for persistence
4. **Use specific image tags** (not latest)
5. **Use networks** to isolate services
6. **Add health checks** for dependencies
7. **Use depends_on** to manage startup order
8. **Document** your services in README
9. **Use override files** for different environments
10. **Keep it simple** - don't over-complicate

## Quick Reference

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f

# List services
docker compose ps

# Stop services
docker compose down

# Rebuild
docker compose build

# Execute command
docker compose exec service-name bash

# View service logs
docker compose logs service-name

# Scale service
docker compose up -d --scale web=3

# Remove everything
docker compose down -v
```

## Next Steps

Continue to [Real World Applications](../03-real-world-apps/README.md) to see complete application examples.
