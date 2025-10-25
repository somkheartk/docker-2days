# วันที่ 1 - Docker Containers

## Docker Container คืออะไร?

Container คือ instance ของ image ที่สามารถรันได้ มันเป็น process ที่แยกออกจากกันที่รันบน host machine โดยแชร์ OS kernel กับ containers อื่นๆ

## Lifecycle ของ Container

```
Create → Start → Running → Stop → Remove
```

## การรัน Containers

### คำสั่ง Run พื้นฐาน

```bash
docker run nginx
```

คำสั่งนี้จะ:
1. ดึง image หากยังไม่มีในเครื่อง
2. สร้าง container
3. เริ่ม container
4. แสดง output ของ container

### Detached Mode

รัน container ใน background:
```bash
docker run -d nginx
docker run -d --name my-nginx nginx
```

### Interactive Mode

รันพร้อมกับเข้าถึง terminal:
```bash
docker run -it ubuntu bash
docker run -it --name my-ubuntu ubuntu bash
```

### Port Mapping

แมป port ของ container ไปยัง port ของ host:
```bash
docker run -d -p 8080:80 nginx
docker run -d -p 127.0.0.1:8080:80 nginx  # Bind ไปยัง IP เฉพาะ
```

แมปหลาย ports:
```bash
docker run -d -p 8080:80 -p 8443:443 nginx
```

## แบบฝึกหัดที่ 1: รัน Web Server

### ขั้นตอนที่ 1: รัน Nginx server
```bash
docker run -d --name web-server -p 8080:80 nginx
```

### ขั้นตอนที่ 2: ทดสอบ
```bash
curl http://localhost:8080
```

### ขั้นตอนที่ 3: เข้าถึง logs
```bash
docker logs web-server
docker logs -f web-server  # ติดตาม logs
```

### ขั้นตอนที่ 4: หยุด container
```bash
docker stop web-server
```

### ขั้นตอนที่ 5: เริ่ม container อีกครั้ง
```bash
docker start web-server
```

## การจัดการ Containers

### แสดงรายการ Containers

แสดง containers ที่กำลังรัน:
```bash
docker ps
```

แสดง containers ทั้งหมด:
```bash
docker ps -a
```

แสดงเฉพาะ Container IDs:
```bash
docker ps -q
```

### หยุด Containers

```bash
docker stop container-name
docker stop container-id
docker stop $(docker ps -q)  # หยุด containers ที่กำลังรันทั้งหมด
```

### ลบ Containers

```bash
docker rm container-name
docker rm -f container-name  # บังคับลบ (แม้กำลังรัน)
docker rm $(docker ps -aq)   # ลบ containers ที่หยุดแล้วทั้งหมด
```

### ทำความสะอาด Container

ลบ containers ที่หยุดแล้ว:
```bash
docker container prune
```

ลบ container อัตโนมัติหลังจาก exit:
```bash
docker run --rm ubuntu echo "สวัสดีชาวโลก"
```

## แบบฝึกหัดที่ 2: สถานะของ Container

### ขั้นตอนที่ 1: สร้าง container โดยไม่เริ่มการทำงาน
```bash
docker create --name test-container nginx
docker ps -a
```

### ขั้นตอนที่ 2: เริ่ม container
```bash
docker start test-container
docker ps
```

### ขั้นตอนที่ 3: หยุดชั่วคราว container
```bash
docker pause test-container
docker ps
```

### ขั้นตอนที่ 4: เริ่มต่อ container
```bash
docker unpause test-container
```

### ขั้นตอนที่ 5: รีสตาร์ท container
```bash
docker restart test-container
```

## การรันคำสั่งใน Containers

รันคำสั่งใน container ที่กำลังทำงาน:
```bash
docker exec container-name command
```

เปิด shell แบบ interactive:
```bash
docker exec -it container-name bash
docker exec -it container-name sh  # สำหรับ Alpine-based images
```

## แบบฝึกหัดที่ 3: ทำงานภายใน Containers

### ขั้นตอนที่ 1: เริ่ม container
```bash
docker run -d --name ubuntu-test ubuntu sleep 3600
```

### ขั้นตอนที่ 2: รันคำสั่ง
```bash
docker exec ubuntu-test ls /
docker exec ubuntu-test cat /etc/os-release
```

### ขั้นตอนที่ 3: เปิด interactive shell
```bash
docker exec -it ubuntu-test bash
```

### ขั้นตอนที่ 4: ติดตั้งและใช้เครื่องมือภายใน container
```bash
apt-get update
apt-get install -y curl
curl --version
exit
```

## Container Logs

### ดู logs
```bash
docker logs container-name
```

### ติดตาม logs แบบ real-time
```bash
docker logs -f container-name
```

### แสดง logs ล่าสุด
```bash
docker logs --tail 50 container-name
```

### แสดง logs พร้อม timestamps
```bash
docker logs -t container-name
```

## แบบฝึกหัดที่ 4: การทำงานกับ Logs

### ขั้นตอนที่ 1: รัน container ที่สร้าง logs
```bash
docker run -d --name log-demo alpine sh -c "while true; do echo 'ข้อความทดสอบ' $(date); sleep 2; done"
```

### ขั้นตอนที่ 2: ดู logs
```bash
docker logs log-demo
docker logs --tail 10 log-demo
docker logs -f log-demo
```

### ขั้นตอนที่ 3: หยุดและลบ
```bash
docker stop log-demo
docker rm log-demo
```

## Environment Variables

### ตั้งค่า environment variables
```bash
docker run -e MY_VAR=value nginx
docker run -e DB_HOST=localhost -e DB_PORT=5432 nginx
```

### ใช้ไฟล์ env
```bash
docker run --env-file .env nginx
```

ตัวอย่างไฟล์ `.env`:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
```

## แบบฝึกหัดที่ 5: Environment Variables

### ขั้นตอนที่ 1: สร้าง container พร้อม env variables
```bash
docker run -it --name env-test -e NAME=Docker -e VERSION=1.0 ubuntu bash
```

### ขั้นตอนที่ 2: ตรวจสอบ variables ภายใน container
```bash
echo $NAME
echo $VERSION
env | grep -E "NAME|VERSION"
exit
```

## Resource Limits

### จำกัด memory
```bash
docker run -d --memory="512m" nginx
docker run -d -m 512m nginx
```

### จำกัด CPU
```bash
docker run -d --cpus="1.5" nginx
docker run -d --cpu-shares=512 nginx
```

### ร่วมกัน
```bash
docker run -d --memory="1g" --cpus="2" nginx
```

## แบบฝึกหัดที่ 6: Resource Limits

### ขั้นตอนที่ 1: รัน container พร้อม resource limits
```bash
docker run -d --name limited-nginx --memory="256m" --cpus="0.5" nginx
```

### ขั้นตอนที่ 2: ตรวจสอบการใช้ resources
```bash
docker stats limited-nginx
```

### ขั้นตอนที่ 3: ดูรายละเอียด container
```bash
docker inspect limited-nginx | grep -A 10 "Memory\|Cpu"
```

## Container Inspection

### ดูข้อมูลทั้งหมดของ container
```bash
docker inspect container-name
```

### ดูข้อมูลเฉพาะส่วน
```bash
docker inspect --format='{{.State.Status}}' container-name
docker inspect --format='{{.NetworkSettings.IPAddress}}' container-name
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container-name
```

## แบบฝึกหัดที่ 7: Container Inspection

### ขั้นตอนที่ 1: สร้าง container
```bash
docker run -d --name inspect-demo nginx
```

### ขั้นตอนที่ 2: ตรวจสอบข้อมูล
```bash
docker inspect inspect-demo
docker inspect --format='{{.State.Status}}' inspect-demo
docker inspect --format='{{.NetworkSettings.IPAddress}}' inspect-demo
```

### ขั้นตอนที่ 3: ดูการใช้ resources
```bash
docker stats inspect-demo --no-stream
```

## Copy Files

### คัดลอกจาก host ไปยัง container
```bash
docker cp file.txt container-name:/path/
docker cp ./folder container-name:/app/
```

### คัดลอกจาก container ไปยัง host
```bash
docker cp container-name:/path/file.txt ./
docker cp container-name:/app/logs ./logs
```

## แบบฝึกหัดที่ 8: การคัดลอกไฟล์

### ขั้นตอนที่ 1: สร้างไฟล์ทดสอบ
```bash
echo "สวัสดี Docker" > test.txt
```

### ขั้นตอนที่ 2: รัน container
```bash
docker run -d --name file-demo nginx
```

### ขั้นตอนที่ 3: คัดลอกไฟล์ไปยัง container
```bash
docker cp test.txt file-demo:/tmp/
```

### ขั้นตอนที่ 4: ตรวจสอบใน container
```bash
docker exec file-demo cat /tmp/test.txt
```

### ขั้นตอนที่ 5: คัดลอกกลับ
```bash
docker cp file-demo:/tmp/test.txt ./retrieved-file.txt
cat retrieved-file.txt
```

## Container Rename

### เปลี่ยนชื่อ container
```bash
docker rename old-name new-name
```

## Container Commit

### สร้าง image จาก container ที่กำลังรัน
```bash
docker commit container-name new-image-name:tag
```

## แบบฝึกหัดที่ 9: Container Commit

### ขั้นตอนที่ 1: สร้างและแก้ไข container
```bash
docker run -it --name custom-ubuntu ubuntu bash
# ภายใน container
apt-get update
apt-get install -y curl vim
exit
```

### ขั้นตอนที่ 2: Commit การเปลี่ยนแปลง
```bash
docker commit custom-ubuntu my-custom-ubuntu:v1
```

### ขั้นตอนที่ 3: ทดสอบ image ใหม่
```bash
docker run -it my-custom-ubuntu:v1 bash
# ตรวจสอบว่า curl และ vim ติดตั้งแล้ว
curl --version
vim --version
exit
```

## Best Practices สำหรับ Containers

1. **ใช้ชื่อที่มีความหมาย**: ใช้ `--name` เพื่อตั้งชื่อ containers
2. **ลบ containers ที่ไม่ใช้**: ใช้ `--rm` หรือ `docker container prune`
3. **จำกัด resources**: กำหนด memory และ CPU limits
4. **อย่า run เป็น root**: ใช้ non-root users ใน containers
5. **ใช้ health checks**: กำหนด health checks สำหรับ containers
6. **เก็บ logs**: ตั้งค่า logging drivers ที่เหมาะสม
7. **อัปเดตเป็นประจำ**: ใช้ images เวอร์ชันล่าสุด

## ขั้นตอนถัดไป

ไปต่อที่ [Docker Volumes](../04-volumes/README.md) เพื่อเรียนรู้วิธีการจัดการข้อมูลถาวรใน Docker
