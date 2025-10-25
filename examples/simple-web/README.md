# Simple Web App Example

This is a basic example of running a static website with Docker.

## Build the image

```bash
docker build -t simple-web .
```

## Run the container

```bash
docker run -d -p 8080:80 --name my-web-app simple-web
```

## Access the application

Open your browser and visit: http://localhost:8080

## Stop and remove

```bash
docker stop my-web-app
docker rm my-web-app
```
