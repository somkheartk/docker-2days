# วันที่ 1 - Docker Images

## Docker Image คืออะไร?

Docker image เป็น template แบบอ่านอย่างเดียวที่ประกอบด้วย:
- โค้ดแอปพลิเคชัน
- Runtime environment
- System tools
- Libraries
- การตั้งค่า

Images ถูก build จากคำสั่งใน Dockerfile และเก็บไว้ใน registries เช่น Docker Hub

## การทำงานกับ Docker Hub

Docker Hub เป็น public registry เริ่มต้นสำหรับ Docker images

### ขั้นตอนที่ 1: ค้นหา Images

ค้นหาบน Docker Hub:
```bash
docker search nginx
docker search ubuntu
```

หรือเยี่ยมชม: https://hub.docker.com

### ขั้นตอนที่ 2: ดาวน์โหลด Images

ดาวน์โหลด image จาก Docker Hub:
```bash
docker pull nginx
docker pull nginx:1.21
docker pull ubuntu:22.04
```

หากไม่ระบุ tag Docker จะดึง tag `latest`

### ขั้นตอนที่ 3: แสดงรายการ Images ในเครื่อง

ดู images ที่ดาวน์โหลดแล้ว:
```bash
docker images
docker image ls
```

## Image Tags และ Versions

Images ใช้ tags เพื่อระบุเวอร์ชัน:
```bash
docker pull nginx:1.21.0       # เวอร์ชันเฉพาะ
docker pull nginx:1.21         # Minor version
docker pull nginx:latest       # เวอร์ชันล่าสุด
docker pull nginx:alpine       # Alpine Linux variant
```

## แบบฝึกหัดที่ 1: สำรวจ Images

### ขั้นตอนที่ 1: ดาวน์โหลดเวอร์ชันต่างๆ
```bash
docker pull nginx:alpine
docker pull nginx:latest
docker images | grep nginx
```

### ขั้นตอนที่ 2: ตรวจสอบ image
```bash
docker image inspect nginx:alpine
```

## ทำความเข้าใจ Dockerfile

Dockerfile เป็นไฟล์ text ที่มีคำสั่งสำหรับ build Docker image

### คำสั่ง Dockerfile พื้นฐาน

- `FROM`: Base image
- `RUN`: รันคำสั่ง
- `COPY`: คัดลอกไฟล์จาก host ไปยัง image
- `ADD`: คล้าย COPY แต่สามารถแตกไฟล์บีบอัดได้
- `WORKDIR`: ตั้งค่า working directory
- `ENV`: ตั้งค่า environment variables
- `EXPOSE`: ระบุ ports ที่ container จะ listen
- `CMD`: คำสั่งเริ่มต้นที่จะรัน
- `ENTRYPOINT`: ตั้งค่า container ให้เป็น executable

## แบบฝึกหัดที่ 2: Dockerfile แรกของคุณ

### ขั้นตอนที่ 1: สร้างไฟล์ app.html
**app.html**
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Docker App</title>
</head>
<body>
    <h1>สวัสดีจาก Docker!</h1>
    <p>นี่คือแอปพลิเคชันที่ containerized แรกของฉัน</p>
</body>
</html>
```

### ขั้นตอนที่ 2: สร้าง Dockerfile
**Dockerfile**
```dockerfile
FROM nginx:alpine
COPY app.html /usr/share/nginx/html/index.html
EXPOSE 80
```

### ขั้นตอนที่ 3: Build image
```bash
docker build -t my-web-app:v1 .
```

### ขั้นตอนที่ 4: รัน container
```bash
docker run -d -p 8080:80 my-web-app:v1
```

### ขั้นตอนที่ 5: ทดสอบ
เยี่ยมชม: http://localhost:8080

## แบบฝึกหัดที่ 3: แอปพลิเคชัน Node.js

### ขั้นตอนที่ 1: สร้างไฟล์ app.js
**app.js**
```javascript
const http = require('http');

const hostname = '0.0.0.0';
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('สวัสดีจาก Node.js Docker Container!\n');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
```

### ขั้นตอนที่ 2: สร้าง Dockerfile
**Dockerfile**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY app.js .
EXPOSE 3000
CMD ["node", "app.js"]
```

### ขั้นตอนที่ 3: Build และรัน
```bash
docker build -t my-node-app .
docker run -d -p 3000:3000 my-node-app
curl http://localhost:3000
```

## Image Layers

Docker images ถูก build เป็น layers โดยแต่ละคำสั่งใน Dockerfile จะสร้าง layer

### ขั้นตอนที่ 1: ดู image history
```bash
docker history nginx:alpine
```

Layers ถูก cache และนำกลับมาใช้ใหม่เพื่อเพิ่มความเร็วในการ build

## การจัดการ Images

### ขั้นตอนที่ 1: ลบ image
```bash
docker rmi nginx:alpine
docker image rm my-web-app:v1
```

### ขั้นตอนที่ 2: ลบ images ที่ไม่ได้ใช้
```bash
docker image prune
docker image prune -a  # ลบ images ทั้งหมดที่ไม่ได้ใช้
```

### ขั้นตอนที่ 3: ติด tag ให้ image
```bash
docker tag my-web-app:v1 my-web-app:latest
docker tag my-web-app:v1 myusername/my-web-app:v1
```

## แบบฝึกหัดที่ 4: Multi-Layer Build

### ขั้นตอนที่ 1: สร้าง Dockerfile แบบหลาย layers
**Dockerfile**
```dockerfile
FROM ubuntu:22.04

# Layer 1: อัปเดตรายการ package
RUN apt-get update

# Layer 2: ติดตั้ง packages
RUN apt-get install -y curl vim

# Layer 3: สร้าง directory
RUN mkdir -p /app/data

# Layer 4: ตั้งค่า working directory
WORKDIR /app

# Layer 5: เพิ่ม metadata
ENV APP_VERSION=1.0

# คำสั่งเริ่มต้น
CMD ["bash"]
```

### ขั้นตอนที่ 2: Build และตรวจสอบ
```bash
docker build -t multi-layer-demo .
docker history multi-layer-demo
```

## Best Practices สำหรับ Images

1. ใช้ official base images
2. ใช้ image tags ที่เฉพาะเจาะจง (ไม่ใช่ `latest`)
3. ลดจำนวน layers ให้น้อยที่สุด
4. ลบไฟล์ที่ไม่จำเป็น
5. ใช้ไฟล์ `.dockerignore`
6. อย่าเก็บ secrets ใน images

## ไฟล์ .dockerignore

### ขั้นตอนที่ 1: สร้างไฟล์ .dockerignore
สร้างไฟล์ `.dockerignore` เพื่อแยกไฟล์ออกจาก build context:

```
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
*.md
```

## ขั้นตอนถัดไป

ไปต่อที่ [Docker Containers](../03-containers/README.md) เพื่อเรียนรู้วิธีการจัดการ containers ที่กำลังรัน
