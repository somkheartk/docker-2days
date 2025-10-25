# วันที่ 1 - แนะนำ Docker

## Docker คืออะไร?

Docker เป็นแพลตฟอร์มสำหรับการพัฒนา จัดส่ง และรันแอปพลิเคชันใน containers โดย Containers ช่วยให้คุณสามารถแพ็คเกจแอปพลิเคชันพร้อมกับ dependencies ทั้งหมดไปสู่หน่วยมาตรฐานสำหรับการพัฒนาซอฟต์แวร์

## แนวคิดหลัก

### Containers เทียบกับ Virtual Machines

**Virtual Machines:**
- รันบน hypervisor
- แต่ละ VM มี OS เต็มรูปแบบ
- ใช้ resources มาก
- เวลา startup ช้า (หลายนาที)

**Containers:**
- รันบน Docker Engine
- แชร์ kernel ของ host OS
- ใช้ resources น้อย
- เวลา startup เร็ว (หลายวินาที)

```
┌─────────────────────────────────────────┐
│         Virtual Machines                │
├─────────────────────────────────────────┤
│  App A  │  App B  │  App C  │           │
│  Bins/  │  Bins/  │  Bins/  │           │
│  Libs   │  Libs   │  Libs   │           │
│  Guest  │  Guest  │  Guest  │           │
│  OS     │  OS     │  OS     │           │
├─────────────────────────────────────────┤
│         Hypervisor                      │
├─────────────────────────────────────────┤
│         Host OS                         │
├─────────────────────────────────────────┤
│         Infrastructure                  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         Docker Containers               │
├─────────────────────────────────────────┤
│  App A  │  App B  │  App C  │           │
│  Bins/  │  Bins/  │  Bins/  │           │
│  Libs   │  Libs   │  Libs   │           │
├─────────────────────────────────────────┤
│         Docker Engine                   │
├─────────────────────────────────────────┤
│         Host OS                         │
├─────────────────────────────────────────┤
│         Infrastructure                  │
└─────────────────────────────────────────┘
```

## สถาปัตยกรรม Docker

Docker ใช้สถาปัตยกรรมแบบ client-server:

1. **Docker Client** - Command-line interface (CLI)
2. **Docker Daemon** - Background service ที่จัดการ containers
3. **Docker Registry** - ที่เก็บข้อมูล Docker images (เช่น Docker Hub)

### ส่วนประกอบหลัก:

- **Image**: Template แบบอ่านอย่างเดียวที่มีคำสั่งสำหรับการสร้าง container
- **Container**: Instance ของ image ที่สามารถรันได้
- **Dockerfile**: ไฟล์ text ที่มีคำสั่งสำหรับ build image
- **Registry**: Repository สำหรับเก็บและแจกจ่าย images
- **Volume**: ที่เก็บข้อมูลถาวรสำหรับข้อมูล container
- **Network**: การสื่อสารระหว่าง containers

## คำสั่ง Docker พื้นฐาน

### ขั้นตอนที่ 1: ตรวจสอบเวอร์ชัน Docker
```bash
docker --version
docker version
docker info
```

## แบบฝึกหัดที่ 1: Hello World

### ขั้นตอนที่ 1: รัน container แรกของคุณ
```bash
docker run hello-world
```

### ขั้นตอนที่ 2: ทำความเข้าใจสิ่งที่เกิดขึ้น
เกิดอะไรขึ้น?
1. Docker client ติดต่อ Docker daemon
2. Docker daemon ดึง image "hello-world" จาก Docker Hub
3. Docker daemon สร้าง container ใหม่จาก image นั้น
4. Docker daemon ส่ง output ไปยัง Docker client

## แบบฝึกหัดที่ 2: Interactive Container

### ขั้นตอนที่ 1: รัน Ubuntu container แบบ interactive
```bash
docker run -it ubuntu bash
```

### ขั้นตอนที่ 2: ลองคำสั่งต่างๆ ภายใน container
```bash
cat /etc/os-release
ls /
exit
```

## แบบฝึกหัดที่ 3: แสดงรายการ Containers

### ขั้นตอนที่ 1: แสดง containers ที่กำลังรัน
```bash
docker ps
```

### ขั้นตอนที่ 2: แสดง containers ทั้งหมด (รวมที่หยุดแล้ว)
```bash
docker ps -a
```

## ประโยชน์ของ Docker

1. **ความสม่ำเสมอ (Consistency)**: สภาพแวดล้อมเดียวกันตั้งแต่การพัฒนาจนถึง production
2. **การแยกส่วน (Isolation)**: แอปพลิเคชันรันในสภาพแวดล้อมที่แยกออกจากกัน
3. **พกพาสะดวก (Portability)**: รันได้ทุกที่ที่ติดตั้ง Docker
4. **ประสิทธิภาพ (Efficiency)**: แชร์ resources ของระบบอย่างมีประสิทธิภาพ
5. **ความเร็ว (Speed)**: startup และ deployment เร็ว
6. **Version Control**: ติดตามเวอร์ชัน image ได้ง่าย

## กรณีการใช้งานทั่วไป

- สถาปัตยกรรม Microservices
- สภาพแวดล้อมการพัฒนา
- Continuous Integration/Continuous Deployment (CI/CD)
- การแยกแอปพลิเคชัน
- การปรับปรุงแอปพลิเคชันเก่า
- แอปพลิเคชันแบบ multi-tenancy

## ขั้นตอนถัดไป

ไปต่อที่ [Docker Images](../02-images/README.md) เพื่อเรียนรู้วิธีการทำงานกับ Docker images
