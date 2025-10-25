# ตัวอย่าง Node.js App

แอปพลิเคชัน Node.js Express แบบง่ายที่รันใน Docker

## ขั้นตอนที่ 1: Build image

```bash
docker build -t node-app .
```

## ขั้นตอนที่ 2: รัน container

```bash
docker run -d -p 3000:3000 --name my-node-app node-app
```

## ขั้นตอนที่ 3: ทดสอบแอปพลิเคชัน

```bash
curl http://localhost:3000
curl http://localhost:3000/health
```

## ขั้นตอนที่ 4: ดู logs

```bash
docker logs -f my-node-app
```

## โหมดพัฒนาด้วย volume mount

```bash
docker run -d -p 3000:3000 -v $(pwd):/app -v /app/node_modules --name node-dev node-app npm run dev
```

## หยุดและลบ

```bash
docker stop my-node-app
docker rm my-node-app
```
