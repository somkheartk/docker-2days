# Python Flask App Example

A simple Python Flask application running in Docker with Gunicorn.

## Build the image

```bash
docker build -t python-app .
```

## Run the container

```bash
docker run -d -p 5000:5000 --name my-python-app python-app
```

## Test the application

```bash
curl http://localhost:5000
curl http://localhost:5000/health
```

## View logs

```bash
docker logs -f my-python-app
```

## Development mode

```bash
docker run -d -p 5000:5000 -v $(pwd):/app -e FLASK_ENV=development --name python-dev python-app flask run --host=0.0.0.0
```

## Stop and remove

```bash
docker stop my-python-app
docker rm my-python-app
```
