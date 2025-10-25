# Docker 2 Days Training Course

Welcome to the Basic Docker for Developer 2-Day Training Course! This repository contains all the materials, examples, and exercises for learning Docker fundamentals.

## Course Overview

This is a hands-on 2-day course designed to teach developers the fundamentals of Docker and containerization. By the end of this course, you will be able to:

- Understand Docker concepts and architecture
- Build and manage Docker images
- Run and manage Docker containers
- Work with Docker volumes and networks
- Use Docker Compose for multi-container applications
- Apply Docker best practices

## Prerequisites

- Basic understanding of Linux command line
- Familiarity with software development concepts
- A computer with Docker installed

## Installing Docker

### Docker Desktop (Windows/Mac)
Download and install Docker Desktop from: https://www.docker.com/products/docker-desktop

### Docker Engine (Linux)
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Verify installation:
```bash
docker --version
docker run hello-world
```

## Course Structure

### Day 1: Docker Basics
1. **Introduction to Docker** (`day1/01-introduction/`)
   - What is Docker?
   - Docker vs Virtual Machines
   - Docker architecture and components

2. **Docker Images** (`day1/02-images/`)
   - Understanding Docker images
   - Working with Docker Hub
   - Creating your first Dockerfile
   - Building images

3. **Docker Containers** (`day1/03-containers/`)
   - Running containers
   - Container lifecycle
   - Managing containers
   - Container logs and debugging

4. **Docker Volumes** (`day1/04-volumes/`)
   - Data persistence in Docker
   - Volume types and management
   - Bind mounts vs volumes

5. **Docker Networks** (`day1/05-networks/`)
   - Container networking basics
   - Network types
   - Container communication

### Day 2: Advanced Docker
1. **Dockerfile Best Practices** (`day2/01-dockerfile-best-practices/`)
   - Multi-stage builds
   - Layer optimization
   - Security considerations

2. **Docker Compose** (`day2/02-docker-compose/`)
   - Introduction to Docker Compose
   - YAML syntax
   - Multi-container applications
   - Service orchestration

3. **Real-World Applications** (`day2/03-real-world-apps/`)
   - Web application with database
   - Microservices example
   - Development workflow

4. **Docker Best Practices** (`day2/04-best-practices/`)
   - Image optimization
   - Security best practices
   - Production considerations

5. **Troubleshooting** (`day2/05-troubleshooting/`)
   - Common issues and solutions
   - Debugging techniques
   - Performance optimization

## Quick Start

### Day 1 Labs
```bash
cd day1
# Follow the exercises in each subdirectory
```

### Day 2 Labs
```bash
cd day2
# Follow the exercises in each subdirectory
```

## Additional Resources

- Official Docker Documentation: https://docs.docker.com
- Docker Hub: https://hub.docker.com
- Docker Cheat Sheet: `./resources/docker-cheatsheet.md`

## Course Reference

This course is based on: https://www.itgenius.co.th/online-courses/basic-docker-for-developer-2026.html

## License

This repository is for educational purposes.

## Support

If you have questions or issues, please open an issue in this repository.

---

Happy Learning! 🐳