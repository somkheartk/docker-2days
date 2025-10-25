# Day 1 - Introduction to Docker

## What is Docker?

Docker is a platform for developing, shipping, and running applications in containers. Containers allow you to package an application with all of its dependencies into a standardized unit for software development.

## Key Concepts

### Containers vs Virtual Machines

**Virtual Machines:**
- Run on a hypervisor
- Each VM includes a full OS
- Heavy resource usage
- Slower startup times (minutes)

**Containers:**
- Run on the Docker Engine
- Share the host OS kernel
- Lightweight resource usage
- Fast startup times (seconds)

```
┌─────────────────────────────────────────┐
│         Virtual Machines                │
├─────────────────────────────────────────┤
│  App A  │  App B  │  App C  │           │
│  Bins/  │  Bins/  │  Bins/  │           │
│  Libs   │  Libs   │  Libs   │           │
│  Guest  │  Guest  │  Guest  │           │
│  OS     │  OS     │  OS     │           │
├─────────────────────────────────────────┤
│         Hypervisor                      │
├─────────────────────────────────────────┤
│         Host OS                         │
├─────────────────────────────────────────┤
│         Infrastructure                  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         Docker Containers               │
├─────────────────────────────────────────┤
│  App A  │  App B  │  App C  │           │
│  Bins/  │  Bins/  │  Bins/  │           │
│  Libs   │  Libs   │  Libs   │           │
├─────────────────────────────────────────┤
│         Docker Engine                   │
├─────────────────────────────────────────┤
│         Host OS                         │
├─────────────────────────────────────────┤
│         Infrastructure                  │
└─────────────────────────────────────────┘
```

## Docker Architecture

Docker uses a client-server architecture:

1. **Docker Client** - Command-line interface (CLI)
2. **Docker Daemon** - Background service managing containers
3. **Docker Registry** - Storage for Docker images (e.g., Docker Hub)

### Key Components:

- **Image**: Read-only template with instructions for creating a container
- **Container**: Runnable instance of an image
- **Dockerfile**: Text file with instructions to build an image
- **Registry**: Repository for storing and distributing images
- **Volume**: Persistent storage for container data
- **Network**: Communication between containers

## Basic Docker Commands

Check Docker version:
```bash
docker --version
docker version
docker info
```

## Exercise 1: Hello World

Run your first container:
```bash
docker run hello-world
```

What happened?
1. Docker client contacted Docker daemon
2. Docker daemon pulled the "hello-world" image from Docker Hub
3. Docker daemon created a new container from that image
4. Docker daemon streamed the output to Docker client

## Exercise 2: Interactive Container

Run an interactive Ubuntu container:
```bash
docker run -it ubuntu bash
```

Inside the container, try:
```bash
cat /etc/os-release
ls /
exit
```

## Exercise 3: List Containers

List running containers:
```bash
docker ps
```

List all containers (including stopped):
```bash
docker ps -a
```

## Benefits of Docker

1. **Consistency**: Same environment from development to production
2. **Isolation**: Applications run in isolated environments
3. **Portability**: Run anywhere Docker is installed
4. **Efficiency**: Share system resources efficiently
5. **Speed**: Fast startup and deployment
6. **Version Control**: Track image versions easily

## Common Use Cases

- Microservices architecture
- Development environments
- Continuous Integration/Continuous Deployment (CI/CD)
- Application isolation
- Legacy application modernization
- Multi-tenancy applications

## Next Steps

Continue to [Docker Images](../02-images/README.md) to learn how to work with Docker images.
