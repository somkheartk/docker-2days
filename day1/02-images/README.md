# Day 1 - Docker Images

## What is a Docker Image?

A Docker image is a read-only template that contains:
- Application code
- Runtime environment
- System tools
- Libraries
- Settings

Images are built from instructions in a Dockerfile and stored in registries like Docker Hub.

## Working with Docker Hub

Docker Hub is the default public registry for Docker images.

### Searching for Images

Search on Docker Hub:
```bash
docker search nginx
docker search ubuntu
```

Or visit: https://hub.docker.com

### Pulling Images

Download an image from Docker Hub:
```bash
docker pull nginx
docker pull nginx:1.21
docker pull ubuntu:22.04
```

Without specifying a tag, Docker pulls the `latest` tag.

### Listing Local Images

View downloaded images:
```bash
docker images
docker image ls
```

## Image Tags and Versions

Images use tags to specify versions:
```bash
docker pull nginx:1.21.0       # Specific version
docker pull nginx:1.21         # Minor version
docker pull nginx:latest       # Latest version
docker pull nginx:alpine       # Alpine Linux variant
```

## Exercise 1: Explore Images

Pull different versions:
```bash
docker pull nginx:alpine
docker pull nginx:latest
docker images | grep nginx
```

Inspect an image:
```bash
docker image inspect nginx:alpine
```

## Understanding Dockerfile

A Dockerfile is a text file with instructions to build a Docker image.

### Basic Dockerfile Instructions

- `FROM`: Base image
- `RUN`: Execute commands
- `COPY`: Copy files from host to image
- `ADD`: Similar to COPY, but can extract archives
- `WORKDIR`: Set working directory
- `ENV`: Set environment variables
- `EXPOSE`: Document which ports the container listens on
- `CMD`: Default command to run
- `ENTRYPOINT`: Configure container as executable

## Exercise 2: Your First Dockerfile

Create a simple web application:

**app.html**
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Docker App</title>
</head>
<body>
    <h1>Hello from Docker!</h1>
    <p>This is my first containerized application.</p>
</body>
</html>
```

**Dockerfile**
```dockerfile
FROM nginx:alpine
COPY app.html /usr/share/nginx/html/index.html
EXPOSE 80
```

Build the image:
```bash
docker build -t my-web-app:v1 .
```

Run the container:
```bash
docker run -d -p 8080:80 my-web-app:v1
```

Visit: http://localhost:8080

## Exercise 3: Node.js Application

**app.js**
```javascript
const http = require('http');

const hostname = '0.0.0.0';
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello from Node.js Docker Container!\n');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
```

**Dockerfile**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY app.js .
EXPOSE 3000
CMD ["node", "app.js"]
```

Build and run:
```bash
docker build -t my-node-app .
docker run -d -p 3000:3000 my-node-app
curl http://localhost:3000
```

## Image Layers

Docker images are built in layers. Each instruction in a Dockerfile creates a layer.

View image history:
```bash
docker history nginx:alpine
```

Layers are cached and reused to speed up builds.

## Managing Images

Remove an image:
```bash
docker rmi nginx:alpine
docker image rm my-web-app:v1
```

Remove unused images:
```bash
docker image prune
docker image prune -a  # Remove all unused images
```

Tag an image:
```bash
docker tag my-web-app:v1 my-web-app:latest
docker tag my-web-app:v1 myusername/my-web-app:v1
```

## Exercise 4: Multi-Layer Build

**Dockerfile**
```dockerfile
FROM ubuntu:22.04

# Layer 1: Update package list
RUN apt-get update

# Layer 2: Install packages
RUN apt-get install -y curl vim

# Layer 3: Create directory
RUN mkdir -p /app/data

# Layer 4: Set working directory
WORKDIR /app

# Layer 5: Add metadata
ENV APP_VERSION=1.0

# Default command
CMD ["bash"]
```

Build and examine:
```bash
docker build -t multi-layer-demo .
docker history multi-layer-demo
```

## Best Practices for Images

1. Use official base images
2. Use specific image tags (not `latest`)
3. Minimize the number of layers
4. Remove unnecessary files
5. Use `.dockerignore` file
6. Don't store secrets in images

## .dockerignore File

Create a `.dockerignore` file to exclude files from the build context:

```
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
*.md
```

## Next Steps

Continue to [Docker Containers](../03-containers/README.md) to learn how to manage running containers.
