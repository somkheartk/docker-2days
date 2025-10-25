# Node.js App Example

A simple Node.js Express application running in Docker.

## Build the image

```bash
docker build -t node-app .
```

## Run the container

```bash
docker run -d -p 3000:3000 --name my-node-app node-app
```

## Test the application

```bash
curl http://localhost:3000
curl http://localhost:3000/health
```

## View logs

```bash
docker logs -f my-node-app
```

## Development mode with volume mount

```bash
docker run -d -p 3000:3000 -v $(pwd):/app -v /app/node_modules --name node-dev node-app npm run dev
```

## Stop and remove

```bash
docker stop my-node-app
docker rm my-node-app
```
