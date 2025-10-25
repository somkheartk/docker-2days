# Day 2 - Real World Applications

## Complete Application Examples

This section contains practical, production-ready examples that demonstrate Docker best practices.

## Example 1: Full-Stack Web Application (MERN Stack)

MongoDB + Express + React + Node.js

### Project Structure
```
mern-app/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── package.json
│   └── server.js
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
└── nginx/
    └── nginx.conf
```

### Backend (backend/server.js)
```javascript
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

// Simple schema
const ItemSchema = new mongoose.Schema({
  name: String,
  description: String
});
const Item = mongoose.model('Item', ItemSchema);

// Routes
app.get('/api/items', async (req, res) => {
  const items = await Item.find();
  res.json(items);
});

app.post('/api/items', async (req, res) => {
  const item = new Item(req.body);
  await item.save();
  res.json(item);
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### Backend Dockerfile (backend/Dockerfile)
```dockerfile
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
EXPOSE 5000
HEALTHCHECK --interval=30s CMD wget --no-verbose --tries=1 --spider http://localhost:5000/health || exit 1
CMD ["node", "server.js"]
```

### Frontend (frontend/Dockerfile)
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose (docker-compose.yml)
```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:6
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password123
    volumes:
      - mongo-data:/data/db
    networks:
      - backend
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    restart: always
    depends_on:
      mongodb:
        condition: service_healthy
    environment:
      MONGODB_URI: mongodb://admin:password123@mongodb:27017/myapp?authSource=admin
      PORT: 5000
    networks:
      - backend
      - frontend
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:5000/health"]
      interval: 30s
      timeout: 3s
      retries: 3

  frontend:
    build: ./frontend
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - frontend

volumes:
  mongo-data:

networks:
  frontend:
  backend:
```

## Example 2: Django + PostgreSQL + Redis

### Project Structure
```
django-app/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
└── myproject/
```

### requirements.txt
```
Django==4.2.0
psycopg2-binary==2.9.6
redis==4.5.5
celery==5.2.7
gunicorn==20.1.0
```

### Dockerfile
```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create non-root user
RUN useradd -m -u 1000 django && \
    chown -R django:django /app
USER django

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "myproject.wsgi:application"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_DB: django_db
      POSTGRES_USER: django_user
      POSTGRES_PASSWORD: django_pass
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U django_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:alpine
    restart: always
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  web:
    build: .
    restart: always
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn --bind 0.0.0.0:8000 --workers 3 myproject.wsgi:application"
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://django_user:django_pass@db:5432/django_db
      REDIS_URL: redis://redis:6379/0
      DJANGO_SETTINGS_MODULE: myproject.settings
      SECRET_KEY: your-secret-key-here
    volumes:
      - ./:/app
      - static-files:/app/staticfiles
    networks:
      - backend
      - frontend

  celery:
    build: .
    restart: always
    command: celery -A myproject worker -l info
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://django_user:django_pass@db:5432/django_db
      REDIS_URL: redis://redis:6379/0
    networks:
      - backend

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - static-files:/app/staticfiles:ro
    depends_on:
      - web
    networks:
      - frontend

volumes:
  postgres-data:
  static-files:

networks:
  frontend:
  backend:
```

## Example 3: Microservices with API Gateway

### docker-compose.yml
```yaml
version: '3.8'

services:
  # API Gateway (Kong)
  kong-database:
    image: postgres:15
    environment:
      POSTGRES_DB: kong
      POSTGRES_USER: kong
      POSTGRES_PASSWORD: kong
    volumes:
      - kong-data:/var/lib/postgresql/data
    networks:
      - kong-net

  kong-migration:
    image: kong:latest
    command: kong migrations bootstrap
    depends_on:
      - kong-database
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_PASSWORD: kong
    networks:
      - kong-net

  kong:
    image: kong:latest
    depends_on:
      - kong-database
      - kong-migration
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_PASSWORD: kong
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_LISTEN: 0.0.0.0:8001
    ports:
      - "8000:8000"  # Proxy
      - "8001:8001"  # Admin API
    networks:
      - kong-net
      - services-net

  # User Service
  user-service:
    build: ./services/users
    environment:
      DATABASE_URL: postgresql://user:pass@user-db:5432/users
    depends_on:
      - user-db
    networks:
      - services-net
    deploy:
      replicas: 2

  user-db:
    image: postgres:15
    environment:
      POSTGRES_DB: users
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - user-data:/var/lib/postgresql/data
    networks:
      - services-net

  # Product Service
  product-service:
    build: ./services/products
    environment:
      DATABASE_URL: postgresql://user:pass@product-db:5432/products
      REDIS_URL: redis://redis:6379
    depends_on:
      - product-db
      - redis
    networks:
      - services-net
    deploy:
      replicas: 2

  product-db:
    image: postgres:15
    environment:
      POSTGRES_DB: products
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - product-data:/var/lib/postgresql/data
    networks:
      - services-net

  # Order Service
  order-service:
    build: ./services/orders
    environment:
      DATABASE_URL: mongodb://order-db:27017/orders
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672
    depends_on:
      - order-db
      - rabbitmq
    networks:
      - services-net
    deploy:
      replicas: 2

  order-db:
    image: mongo:6
    volumes:
      - order-data:/data/db
    networks:
      - services-net

  # Shared Services
  redis:
    image: redis:alpine
    networks:
      - services-net

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "15672:15672"
    networks:
      - services-net

  # Monitoring
  prometheus:
    image: prom/prometheus
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - services-net

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    networks:
      - services-net

volumes:
  kong-data:
  user-data:
  product-data:
  order-data:
  prometheus-data:
  grafana-data:

networks:
  kong-net:
  services-net:
```

## Example 4: CI/CD Pipeline with GitLab Runner

### .gitlab-ci.yml
```yaml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE:latest

test:
  stage: test
  image: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  script:
    - npm test

deploy:
  stage: deploy
  image: docker/compose:latest
  script:
    - docker-compose -f docker-compose.prod.yml pull
    - docker-compose -f docker-compose.prod.yml up -d
  only:
    - main
```

## Example 5: E-commerce Platform

Complete e-commerce with frontend, backend, payment service, and admin panel.

### docker-compose.yml
```yaml
version: '3.8'

services:
  # Frontend
  storefront:
    build: ./storefront
    ports:
      - "3000:80"
    depends_on:
      - api-gateway
    networks:
      - frontend

  admin-panel:
    build: ./admin
    ports:
      - "3001:80"
    depends_on:
      - api-gateway
    networks:
      - frontend

  # Backend Services
  api-gateway:
    build: ./gateway
    ports:
      - "4000:4000"
    depends_on:
      - auth-service
      - product-service
      - order-service
      - payment-service
    networks:
      - frontend
      - backend

  auth-service:
    build: ./services/auth
    environment:
      DATABASE_URL: postgresql://user:pass@auth-db:5432/auth
      JWT_SECRET: your-jwt-secret
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - auth-db
      - redis
    networks:
      - backend

  product-service:
    build: ./services/products
    environment:
      DATABASE_URL: postgresql://user:pass@product-db:5432/products
      ELASTICSEARCH_URL: http://elasticsearch:9200
      REDIS_URL: redis://redis:6379/1
    depends_on:
      - product-db
      - elasticsearch
      - redis
    networks:
      - backend
    deploy:
      replicas: 3

  order-service:
    build: ./services/orders
    environment:
      DATABASE_URL: postgresql://user:pass@order-db:5432/orders
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672
    depends_on:
      - order-db
      - rabbitmq
    networks:
      - backend

  payment-service:
    build: ./services/payment
    environment:
      DATABASE_URL: postgresql://user:pass@payment-db:5432/payments
      STRIPE_API_KEY: ${STRIPE_API_KEY}
    depends_on:
      - payment-db
    networks:
      - backend

  notification-service:
    build: ./services/notifications
    environment:
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672
      SENDGRID_API_KEY: ${SENDGRID_API_KEY}
    depends_on:
      - rabbitmq
    networks:
      - backend

  # Databases
  auth-db:
    image: postgres:15
    environment:
      POSTGRES_DB: auth
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - auth-data:/var/lib/postgresql/data
    networks:
      - backend

  product-db:
    image: postgres:15
    environment:
      POSTGRES_DB: products
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - product-data:/var/lib/postgresql/data
    networks:
      - backend

  order-db:
    image: postgres:15
    environment:
      POSTGRES_DB: orders
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - order-data:/var/lib/postgresql/data
    networks:
      - backend

  payment-db:
    image: postgres:15
    environment:
      POSTGRES_DB: payments
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - payment-data:/var/lib/postgresql/data
    networks:
      - backend

  # Infrastructure
  redis:
    image: redis:alpine
    volumes:
      - redis-data:/data
    networks:
      - backend

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "15672:15672"
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    networks:
      - backend

  elasticsearch:
    image: elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    networks:
      - backend

  # Monitoring
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    networks:
      - backend

  grafana:
    image: grafana/grafana
    ports:
      - "3002:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana-data:/var/lib/grafana
    networks:
      - backend

volumes:
  auth-data:
  product-data:
  order-data:
  payment-data:
  redis-data:
  rabbitmq-data:
  elasticsearch-data:
  prometheus-data:
  grafana-data:

networks:
  frontend:
  backend:
```

## Development Workflow

### Local Development Setup
```bash
# Clone repository
git clone https://github.com/yourcompany/app.git
cd app

# Copy environment file
cp .env.example .env

# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Run database migrations
docker compose exec web python manage.py migrate

# Create admin user
docker compose exec web python manage.py createsuperuser

# Run tests
docker compose exec web npm test
```

### Hot Reloading for Development
```yaml
services:
  web:
    build: .
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev
```

## Production Deployment

### docker-compose.prod.yml
```yaml
version: '3.8'

services:
  web:
    image: registry.company.com/app:${VERSION}
    restart: always
    environment:
      - NODE_ENV=production
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

Deploy:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Best Practices for Real-World Apps

1. **Use health checks** for all services
2. **Implement proper logging** with log drivers
3. **Set resource limits** to prevent resource exhaustion
4. **Use secrets management** (Docker secrets, vault)
5. **Implement monitoring** (Prometheus, Grafana)
6. **Use load balancers** for high availability
7. **Backup databases** regularly
8. **Version your images** properly
9. **Use CI/CD pipelines** for deployments
10. **Document everything** in README

## Next Steps

Continue to [Best Practices](../04-best-practices/README.md) for production guidelines.
