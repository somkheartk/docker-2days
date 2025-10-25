# ตัวอย่าง Web App แบบง่าย

นี่คือตัวอย่างพื้นฐานของการรันเว็บไซต์แบบคงที่ด้วย Docker

## ขั้นตอนที่ 1: Build image

```bash
docker build -t simple-web .
```

## ขั้นตอนที่ 2: รัน container

```bash
docker run -d -p 8080:80 --name my-web-app simple-web
```

## ขั้นตอนที่ 3: เข้าถึงแอปพลิเคชัน

เปิดเบราว์เซอร์และไปที่: http://localhost:8080

## ขั้นตอนที่ 4: หยุดและลบ

```bash
docker stop my-web-app
docker rm my-web-app
```
