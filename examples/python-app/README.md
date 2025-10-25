# ตัวอย่าง Python Flask App

แอปพลิเคชัน Python Flask แบบง่ายที่รันใน Docker ด้วย Gunicorn

## ขั้นตอนที่ 1: Build image

```bash
docker build -t python-app .
```

## ขั้นตอนที่ 2: รัน container

```bash
docker run -d -p 5000:5000 --name my-python-app python-app
```

## ขั้นตอนที่ 3: ทดสอบแอปพลิเคชัน

```bash
curl http://localhost:5000
curl http://localhost:5000/health
```

## ขั้นตอนที่ 4: ดู logs

```bash
docker logs -f my-python-app
```

## โหมดพัฒนา

```bash
docker run -d -p 5000:5000 -v $(pwd):/app -e FLASK_ENV=development --name python-dev python-app flask run --host=0.0.0.0
```

## หยุดและลบ

```bash
docker stop my-python-app
docker rm my-python-app
```
