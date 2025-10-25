# Docker Cheat Sheet

## คู่มืออ้างอิงด่วน

### พื้นฐาน Container

```bash
# รัน container
docker run image                    # รัน container จาก image
docker run -d image                # รันในโหมด detached
docker run -it image /bin/bash     # Interactive พร้อม terminal
docker run --name myapp image      # ตั้งชื่อเอง
docker run --rm image              # ลบหลัง exit
docker run -p 8080:80 image        # แมป port
docker run -v /host:/container image  # mount volume
docker run -e KEY=value image      # ตั้งค่า environment variable

# จัดการ Container
docker ps                          # แสดง containers ที่กำลังรัน
docker ps -a                       # แสดง containers ทั้งหมด
docker start container             # เริ่ม container ที่หยุด
docker stop container              # หยุด container ที่กำลังรัน
docker restart container           # รีสตาร์ท container
docker rm container                # ลบ container
docker rm -f container             # บังคับลบ container ที่กำลังรัน
docker exec -it container bash     # รันคำสั่งใน container
docker logs container              # ดู container logs
docker logs -f container           # ติดตาม logs
docker inspect container           # ดูข้อมูลละเอียด
docker stats container             # ดูการใช้ resources
docker top container               # แสดงรายการ process
```

### การจัดการ Images

```bash
# การทำงานกับ Image
docker images                      # แสดง images ในเครื่อง
docker pull image                  # ดาวน์โหลด image
docker pull image:tag              # ดาวน์โหลดเวอร์ชันเฉพาะ
docker push image                  # อัปโหลด image ไปยัง registry
docker build -t name:tag .         # build image
docker build --no-cache -t name .  # build โดยไม่ใช้ cache
docker rmi image                   # ลบ image
docker tag source target           # ติด tag ให้ image
docker history image               # แสดง image layers
docker save -o file.tar image      # บันทึก image เป็นไฟล์
docker load -i file.tar            # โหลด image จากไฟล์
docker search term                 # ค้นหาใน Docker Hub
docker image prune                 # ลบ images ที่ไม่ได้ใช้
docker image prune -a              # ลบ images ที่ไม่ได้ใช้ทั้งหมด
```

### คำสั่ง Dockerfile

```dockerfile
FROM image:tag              # Base image
LABEL key="value"          # Metadata
ENV KEY=value              # Environment variable
ARG KEY=value              # Build argument
WORKDIR /path              # Working directory
COPY src dest              # คัดลอกไฟล์
ADD src dest               # คัดลอกไฟล์ (มีฟีเจอร์เพิ่ม)
RUN command                # รันคำสั่ง
CMD ["executable"]         # คำสั่งเริ่มต้น
ENTRYPOINT ["executable"]  # Container executable
EXPOSE port                # ระบุ ports
VOLUME /path               # สร้าง mount point
USER username              # ตั้งค่า user
HEALTHCHECK CMD command    # Health check
SHELL ["executable"]       # ตั้งค่า shell
```

### Docker Compose

```bash
# คำสั่งพื้นฐาน
docker compose up                  # เริ่ม services
docker compose up -d              # เริ่มใน background
docker compose down               # หยุดและลบ
docker compose down -v            # ลบ volumes ด้วย
docker compose start              # เริ่ม services
docker compose stop               # หยุด services
docker compose restart            # รีสตาร์ท services
docker compose ps                 # แสดง containers
docker compose logs               # ดู logs
docker compose logs -f            # ติดตาม logs
docker compose logs service       # ดู logs ของ service
docker compose exec service cmd   # รันคำสั่ง
docker compose run service cmd    # รันคำสั่งครั้งเดียว
docker compose build              # build images
docker compose build --no-cache   # build โดยไม่ใช้ cache
docker compose pull               # ดึง images
docker compose push               # push images
docker compose config             # ตรวจสอบและดู config
docker compose top                # แสดง processes
```

### โครงสร้าง docker-compose.yml

```yaml
version: '3.8'
services:
  web:
    image: nginx
    build: 
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:80"
    volumes:
      - ./app:/usr/share/nginx/html
      - data:/var/lib/data
    environment:
      - NODE_ENV=production
    env_file:
      - .env
    depends_on:
      - db
    networks:
      - frontend
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3
      
  db:
    image: postgres:15
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: secret

volumes:
  data:
  db-data:

networks:
  frontend:
  backend:
```

### Docker Volumes

```bash
# การจัดการ Volume
docker volume create name         # สร้าง volume
docker volume ls                  # แสดง volumes
docker volume inspect name        # ตรวจสอบ volume
docker volume rm name             # ลบ volume
docker volume prune               # ลบ volumes ที่ไม่ได้ใช้

# ใช้ Volumes
docker run -v name:/path image    # Named volume
docker run -v /host:/container image  # Bind mount
docker run -v /container image    # Anonymous volume
docker run -v name:/path:ro image # Read-only
```

### Docker Networks

```bash
# การจัดการ Network
docker network create name        # สร้าง network
docker network ls                 # แสดง networks
docker network inspect name       # ตรวจสอบ network
docker network rm name            # ลบ network
docker network prune              # ลบ networks ที่ไม่ได้ใช้
docker network connect net cont   # เชื่อมต่อ container
docker network disconnect net cont # ตัดการเชื่อมต่อ

# ประเภท Networks
docker network create --driver bridge name
docker network create --driver host name
docker network create --driver overlay name
```

### System Commands

```bash
# ข้อมูลระบบ
docker info                       # ข้อมูลระบบ Docker
docker version                    # เวอร์ชัน Docker
docker system df                  # การใช้พื้นที่
docker system df -v               # การใช้พื้นที่แบบละเอียด
docker system prune               # ทำความสะอาดระบบ
docker system prune -a            # ทำความสะอาดทั้งหมด
docker system prune -a --volumes  # รวม volumes

# Events และ monitoring
docker events                     # ดู events แบบ real-time
docker stats                      # สถิติ containers ทั้งหมด
docker top container              # Process ใน container
```

### Registry และ Login

```bash
# Docker Hub
docker login                      # เข้าสู่ระบบ Docker Hub
docker logout                     # ออกจากระบบ
docker search term                # ค้นหา images
docker pull username/image:tag    # ดึง image
docker push username/image:tag    # push image

# Private Registry
docker login registry.example.com
docker tag image registry.example.com/image:tag
docker push registry.example.com/image:tag
```

### Best Practices

#### สำหรับ Dockerfiles
```dockerfile
# 1. ใช้ official base images
FROM node:18-alpine

# 2. จัดกลุ่มคำสั่ง RUN
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*

# 3. ใช้ multi-stage builds
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-alpine
COPY --from=builder /app/dist /app
CMD ["node", "app/server.js"]

# 4. ใช้ .dockerignore
# node_modules
# .git
# *.md
```

#### สำหรับ Production
- ใช้ specific image tags ไม่ใช่ `latest`
- รัน containers เป็น non-root user
- ใช้ health checks
- ตั้งค่า resource limits
- ใช้ multi-stage builds เพื่อลดขนาด
- อย่าเก็บ secrets ใน images
- scan images หา vulnerabilities

### Troubleshooting

```bash
# Debug Container
docker logs container             # ดู logs
docker logs --tail 100 container  # 100 บรรทัดล่าสุด
docker logs -f container          # ติดตาม logs
docker exec -it container sh      # เข้าไปใน container
docker inspect container          # ข้อมูลทั้งหมด
docker top container              # processes
docker stats container            # การใช้ resources

# Network Debug
docker network inspect network    # ตรวจสอบ network
docker exec container ping host   # ทดสอบการเชื่อมต่อ
docker port container             # ดู port mappings

# ทำความสะอาด
docker system prune               # ลบทรัพยากรที่ไม่ได้ใช้
docker container prune            # ลบ containers ที่หยุด
docker image prune                # ลบ images ที่ไม่ได้ใช้
docker volume prune               # ลบ volumes ที่ไม่ได้ใช้
docker network prune              # ลบ networks ที่ไม่ได้ใช้
```

### รูปแบบที่ใช้บ่อย

```bash
# ลบ containers ทั้งหมด
docker rm -f $(docker ps -aq)

# ลบ images ทั้งหมด
docker rmi -f $(docker images -q)

# ดู IPs ของ containers ทั้งหมด
docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -q)

# หยุด containers ทั้งหมด
docker stop $(docker ps -q)

# Backup volume
docker run --rm -v volume:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz -C /data .

# Restore volume
docker run --rm -v volume:/data -v $(pwd):/backup alpine sh -c "cd /data && tar xzf /backup/backup.tar.gz"
```

### Environment Variables

```bash
# ใน command line
docker run -e VAR=value image
docker run -e VAR1=value1 -e VAR2=value2 image

# จากไฟล์
docker run --env-file .env image

# ใน docker-compose.yml
environment:
  - VAR=value
  - VAR2=value2
# หรือ
env_file:
  - .env
```

### Health Checks

```dockerfile
# ใน Dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
```

```yaml
# ใน docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## แหล่งข้อมูลเพิ่มเติม

- เอกสารอย่างเป็นทางการ: https://docs.docker.com
- Docker Hub: https://hub.docker.com
- Docker Samples: https://github.com/docker/samples

---

จัดทำโดยคอร์สเรียน Docker 2 วัน 🐳
