# Docker 2-Day Training Course - Summary

## What Has Been Created

This repository contains a complete, comprehensive 2-day Docker training course designed for developers who want to learn Docker from basics to production-ready deployments.

## Repository Structure

```
docker-2days/
├── README.md                          # Main course overview and navigation
├── COURSE_SUMMARY.md                  # This file
├── .gitignore                         # Git ignore configuration
│
├── day1/                              # Day 1: Docker Fundamentals
│   ├── 01-introduction/              # Docker basics and architecture
│   ├── 02-images/                    # Working with Docker images
│   ├── 03-containers/                # Container management
│   ├── 04-volumes/                   # Data persistence
│   └── 05-networks/                  # Container networking
│
├── day2/                              # Day 2: Advanced Docker
│   ├── 01-dockerfile-best-practices/ # Optimizing Dockerfiles
│   ├── 02-docker-compose/            # Multi-container applications
│   ├── 03-real-world-apps/           # Production examples
│   ├── 04-best-practices/            # Production guidelines
│   └── 05-troubleshooting/           # Debugging and problem-solving
│
├── examples/                          # Hands-on code examples
│   ├── simple-web/                   # Static HTML with Nginx
│   ├── node-app/                     # Node.js Express application
│   └── python-app/                   # Python Flask application
│
└── resources/                         # Additional materials
    └── docker-cheatsheet.md          # Quick reference guide
```

## Course Content

### Day 1: Docker Basics (5 modules)

1. **Introduction to Docker**
   - What is Docker and why use it
   - Docker vs Virtual Machines
   - Docker architecture components
   - Basic Docker commands
   - First container exercises

2. **Docker Images**
   - Understanding Docker images
   - Working with Docker Hub
   - Creating Dockerfiles
   - Building images
   - Image layers and caching
   - Managing images

3. **Docker Containers**
   - Container lifecycle
   - Running containers (detached, interactive)
   - Port mapping
   - Container management commands
   - Executing commands in containers
   - Container logs and debugging
   - Environment variables
   - Resource limits

4. **Docker Volumes**
   - Data persistence concepts
   - Volume types (named, anonymous, bind mounts)
   - Creating and managing volumes
   - Sharing volumes between containers
   - Backup and restore procedures

5. **Docker Networks**
   - Container networking basics
   - Network drivers (bridge, host, none)
   - User-defined networks
   - Container communication
   - DNS resolution
   - Network isolation patterns

### Day 2: Advanced Docker (5 modules)

1. **Dockerfile Best Practices**
   - Layer optimization
   - Multi-stage builds
   - Choosing base images
   - .dockerignore usage
   - Running as non-root user
   - Security considerations
   - Image size optimization

2. **Docker Compose**
   - Introduction to Docker Compose
   - YAML configuration
   - Service definitions
   - Multi-container applications
   - Environment variables
   - Volumes and networks in Compose
   - Docker Compose commands
   - Development vs Production configs

3. **Real-World Applications**
   - MERN Stack (MongoDB, Express, React, Node.js)
   - Django + PostgreSQL + Redis
   - Microservices architecture
   - E-commerce platform example
   - CI/CD integration
   - Development workflows

4. **Best Practices**
   - Security best practices
   - Image optimization techniques
   - Resource management
   - Networking strategies
   - Data persistence patterns
   - Environment configuration
   - Monitoring and logging
   - Production checklist

5. **Troubleshooting**
   - Common issues and solutions
   - Container startup problems
   - Network debugging
   - Volume and permission issues
   - Image build failures
   - Performance issues
   - Debugging techniques
   - Recovery procedures

## Practical Examples

### 1. Simple Web (HTML + Nginx)
A basic static website served by Nginx, demonstrating:
- Basic Dockerfile creation
- Building and running containers
- Port mapping
- Volume mounting

### 2. Node.js Application
An Express.js API application showing:
- Node.js Dockerfile patterns
- Multi-stage builds
- Health checks
- Non-root user configuration
- Development vs production modes

### 3. Python Flask Application
A Flask REST API demonstrating:
- Python application containerization
- Gunicorn for production
- Virtual environment handling
- Health check endpoints
- Security best practices

## Resources

### Docker Cheat Sheet
Comprehensive quick reference covering:
- All essential Docker commands
- Dockerfile instructions
- Docker Compose syntax
- Common patterns and troubleshooting
- Best practices reminders

## Learning Path

### For Beginners
1. Start with README.md for course overview
2. Follow Day 1 modules in order (01 → 05)
3. Try examples in the `examples/` directory
4. Complete Day 2 modules in order
5. Reference the cheat sheet as needed

### For Intermediate Users
1. Review Day 1 modules quickly
2. Focus on Day 2 advanced topics
3. Study real-world application examples
4. Implement best practices in your projects
5. Use troubleshooting guide as reference

### For Hands-On Practice
1. Each module has practical exercises
2. Three complete working examples provided
3. Can be extended and modified for learning
4. Examples use common tech stacks

## Key Learning Outcomes

After completing this course, learners will be able to:

✅ Understand Docker concepts and architecture
✅ Build optimized Docker images
✅ Run and manage containers effectively
✅ Implement data persistence strategies
✅ Configure container networking
✅ Use Docker Compose for multi-container apps
✅ Apply security best practices
✅ Troubleshoot common Docker issues
✅ Deploy production-ready applications
✅ Follow industry best practices

## Course Features

- **Comprehensive**: Covers basics to advanced topics
- **Hands-on**: Practical exercises in every module
- **Real-world**: Production-ready examples
- **Well-structured**: Progressive learning path
- **Reference materials**: Quick reference cheat sheet
- **Best practices**: Security and optimization guidelines
- **Troubleshooting**: Common problems and solutions

## Technology Stack Covered

- **Languages**: Node.js, Python, HTML/CSS
- **Frameworks**: Express.js, Flask
- **Databases**: PostgreSQL, MongoDB, MySQL, Redis
- **Web Servers**: Nginx
- **Tools**: Docker, Docker Compose
- **Platforms**: Linux, macOS, Windows

## Recommended Prerequisites

- Basic command line knowledge
- Familiarity with at least one programming language
- Understanding of web application concepts
- Basic understanding of networking (helpful but not required)

## Course Duration

- **Day 1**: 6-8 hours (with hands-on exercises)
- **Day 2**: 6-8 hours (with hands-on exercises)
- **Total**: 12-16 hours of comprehensive training

## Source

This course is based on the curriculum from:
https://www.itgenius.co.th/online-courses/basic-docker-for-developer-2026.html

## License

This repository is for educational purposes.

---

**Happy Learning! 🐳**

Start your Docker journey by opening the [README.md](README.md) file!
