# วันที่ 1 - Docker Volumes

## ปัญหา: การเก็บข้อมูลถาวร

โดยค่าเริ่มต้น ข้อมูลใน container จะหายไปเมื่อลบ container Volumes ช่วยแก้ปัญหานี้โดยการให้ที่เก็บข้อมูลถาวร

## Docker Volumes คืออะไร?

Volumes เป็นกลไกที่แนะนำสำหรับการเก็บข้อมูลถาวรที่สร้างและใช้โดย Docker containers

### ประโยชน์ของ Volumes:
- ข้อมูลคงอยู่แม้หลังจากลบ container
- สามารถแชร์ระหว่าง containers ได้
- สำรองและย้ายข้อมูลได้ง่ายขึ้น
- ทำงานได้ทั้ง Linux และ Windows containers
- สามารถจัดการได้โดยใช้ Docker CLI

## ประเภทของ Storage

### 1. Volumes (แนะนำ)
จัดการโดย Docker เก็บใน storage directory ของ Docker

### 2. Bind Mounts
แมป directory ของ host ไปยัง directory ของ container

### 3. tmpfs Mounts
เก็บใน memory ของ host เท่านั้น (Linux เท่านั้น)

```
┌─────────────────────────────────────────┐
│          Container                      │
│  ┌─────────────────────────────────┐   │
│  │  /app/data  (Volume)            │   │
│  │  /app/config (Bind Mount)       │   │
│  │  /tmp (tmpfs)                   │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
         │         │         │
         ▼         ▼         ▼
    Docker     Host      Host
    Volume     Dir       Memory
```

## การทำงานกับ Volumes

### ขั้นตอนที่ 1: สร้าง Volume

```bash
docker volume create my-volume
```

### ขั้นตอนที่ 2: แสดงรายการ Volumes

```bash
docker volume ls
```

### ขั้นตอนที่ 3: ตรวจสอบ Volume

```bash
docker volume inspect my-volume
```

### ขั้นตอนที่ 4: ลบ Volume

```bash
docker volume rm my-volume
docker volume prune  # ลบ volumes ที่ไม่ได้ใช้ทั้งหมด
```

## แบบฝึกหัดที่ 1: ใช้ Named Volumes

### ขั้นตอนที่ 1: รัน container พร้อม volume
```bash
docker run -d --name mysql-db \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret123 \
  mysql:8
```

### ขั้นตอนที่ 2: สร้างข้อมูล
```bash
docker exec -it mysql-db mysql -uroot -psecret123 -e "CREATE DATABASE testdb;"
docker exec -it mysql-db mysql -uroot -psecret123 -e "SHOW DATABASES;"
```

### ขั้นตอนที่ 3: ลบ container
```bash
docker rm -f mysql-db
```

### ขั้นตอนที่ 4: สร้าง container ใหม่ด้วย volume เดิม
```bash
docker run -d --name mysql-db-new \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret123 \
  mysql:8
```

### ขั้นตอนที่ 5: ตรวจสอบว่าข้อมูลยังคงอยู่
```bash
docker exec -it mysql-db-new mysql -uroot -psecret123 -e "SHOW DATABASES;"
```

## Bind Mounts

Bind mounts แมป directory หรือไฟล์จาก host system ไปยัง container

### ขั้นตอนที่ 1: สร้าง directory
```bash
mkdir -p $(pwd)/html
echo "<h1>สวัสดีจาก Bind Mount</h1>" > $(pwd)/html/index.html
```

### ขั้นตอนที่ 2: รัน container พร้อม bind mount
```bash
docker run -d --name web \
  -p 8080:80 \
  -v $(pwd)/html:/usr/share/nginx/html \
  nginx
```

### ขั้นตอนที่ 3: ทดสอบ
```bash
curl http://localhost:8080
```

### ขั้นตอนที่ 4: แก้ไขไฟล์
```bash
echo "<h1>อัปเดตเนื้อหา</h1>" > $(pwd)/html/index.html
curl http://localhost:8080
```

## แบบฝึกหัดที่ 2: พัฒนา Node.js Application

### ขั้นตอนที่ 1: สร้างโครงสร้างโปรเจกต์
```bash
mkdir -p node-dev && cd node-dev
```

### ขั้นตอนที่ 2: สร้าง package.json
```json
{
  "name": "node-dev",
  "version": "1.0.0",
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {
    "express": "^4.18.0"
  }
}
```

### ขั้นตอนที่ 3: สร้าง app.js
```javascript
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('สวัสดีจาก Node.js!');
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

### ขั้นตอนที่ 4: สร้าง Dockerfile
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
```

### ขั้นตอนที่ 5: Build และรัน
```bash
docker build -t node-dev .
docker run -d -p 3000:3000 \
  -v $(pwd):/app \
  -v /app/node_modules \
  --name node-dev \
  node-dev
```

### ขั้นตอนที่ 6: ทดสอบการอัปเดตแบบ hot-reload
แก้ไข `app.js` และรีเฟรชเบราว์เซอร์

## การแชร์ Volumes ระหว่าง Containers

### ขั้นตอนที่ 1: สร้าง shared volume
```bash
docker volume create shared-data
```

### ขั้นตอนที่ 2: รัน container แรก (writer)
```bash
docker run -d --name writer \
  -v shared-data:/data \
  alpine sh -c "while true; do date >> /data/log.txt; sleep 5; done"
```

### ขั้นตอนที่ 3: รัน container ที่สอง (reader)
```bash
docker run -d --name reader \
  -v shared-data:/data \
  alpine sh -c "while true; do tail -f /data/log.txt; sleep 1; done"
```

### ขั้นตอนที่ 4: ตรวจสอบ logs
```bash
docker logs -f reader
```

## แบบฝึกหัดที่ 3: Backup และ Restore

### ขั้นตอนที่ 1: สร้างข้อมูลใน volume
```bash
docker run -v backup-demo:/data \
  alpine sh -c "echo 'ข้อมูลสำคัญ' > /data/important.txt"
```

### ขั้นตอนที่ 2: Backup volume
```bash
docker run --rm \
  -v backup-demo:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz -C /data .
```

### ขั้นตอนที่ 3: สร้าง volume ใหม่
```bash
docker volume create restored-data
```

### ขั้นตอนที่ 4: Restore ข้อมูล
```bash
docker run --rm \
  -v restored-data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/backup.tar.gz"
```

### ขั้นตอนที่ 5: ตรวจสอบข้อมูลที่ restore
```bash
docker run --rm -v restored-data:/data alpine cat /data/important.txt
```

## Volume Drivers

Docker รองรับ volume drivers หลายประเภทสำหรับ storage backends ต่างๆ

### Local Driver (ค่าเริ่มต้น)
```bash
docker volume create --driver local my-local-volume
```

### ตัวอย่าง Volume Drivers อื่นๆ
- NFS
- AWS EBS
- Azure File Storage
- GlusterFS
- Ceph

## แบบฝึกหัดที่ 4: Read-only Volumes

### ขั้นตอนที่ 1: สร้างไฟล์ config
```bash
mkdir config
echo "database=production" > config/app.conf
```

### ขั้นตอนที่ 2: Mount เป็น read-only
```bash
docker run -it --rm \
  -v $(pwd)/config:/config:ro \
  alpine sh
```

### ขั้นตอนที่ 3: ทดสอบภายใน container
```bash
# ภายใน container
cat /config/app.conf
# ลองเขียน (จะล้มเหลว)
echo "test" > /config/test.txt
exit
```

## Best Practices สำหรับ Volumes

1. **ใช้ Named Volumes**: ง่ายต่อการจัดการและบำรุงรักษา
2. **ใช้ Volumes สำหรับข้อมูลถาวร**: ไม่ใช่ bind mounts ใน production
3. **Backup เป็นประจำ**: สร้างกระบวนการ backup อัตโนมัติ
4. **ใช้ Read-only Mounts**: สำหรับไฟล์ configuration
5. **ทำความสะอาด Volumes**: ใช้ `docker volume prune` เป็นประจำ
6. **ตั้งชื่อที่มีความหมาย**: ใช้ชื่อที่บ่งบอกถึงวัตถุประสงค์
7. **Monitor ขนาด**: ตรวจสอบการใช้พื้นที่เก็บข้อมูล

## Volume vs Bind Mount: เมื่อไหร่ควรใช้อะไร

### ใช้ Volumes เมื่อ:
- ต้องการเก็บข้อมูลถาวรใน production
- แชร์ข้อมูลระหว่างหลาย containers
- ต้องการ backup/restore ง่ายๆ
- ใช้ remote storage

### ใช้ Bind Mounts เมื่อ:
- การพัฒนาแบบ local development
- ต้องการเข้าถึงไฟล์ configuration จาก host
- แชร์ source code สำหรับ hot-reloading
- ต้องการควบคุมตำแหน่งไฟล์อย่างเจาะจง

## Troubleshooting

### ปัญหา: Volume ไม่ถูกลบ
```bash
# ดู containers ที่ใช้ volume
docker ps -a --filter volume=VOLUME_NAME

# หยุดและลบ containers ที่เกี่ยวข้อง
docker rm -f $(docker ps -aq --filter volume=VOLUME_NAME)

# ลบ volume
docker volume rm VOLUME_NAME
```

### ปัญหา: Permission denied
```bash
# ตรวจสอบ permissions
docker run --rm -v my-volume:/data alpine ls -la /data

# แก้ไข ownership
docker run --rm -v my-volume:/data alpine chown -R 1000:1000 /data
```

### ปัญหา: Volume เต็ม
```bash
# ตรวจสอบขนาด
docker system df -v

# ทำความสะอาด
docker volume prune
```

## ขั้นตอนถัดไป

ไปต่อที่ [Docker Networks](../05-networks/README.md) เพื่อเรียนรู้วิธีการเชื่อมต่อ containers เข้าด้วยกัน
