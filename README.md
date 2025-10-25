# คอร์สเรียน Docker 2 วัน

## 📑 สารบัญ (Table of Contents)

- [ภาพรวมคอร์ส](#ภาพรวมคอร์ส)
- [สิ่งที่ต้องมีก่อนเรียน](#สิ่งที่ต้องมีก่อนเรียน)
- [การติดตั้ง Docker](#การติดตั้ง-docker)
- [โครงสร้างคอร์ส](#โครงสร้างคอร์ส)
  - [วันที่ 1: Docker พื้นฐาน](#วันที่-1-docker-พื้นฐาน)
  - [วันที่ 2: Docker ขั้นสูง](#วันที่-2-docker-ขั้นสูง)
- [ตัวอย่างเชิงปฏิบัติ](#ตัวอย่างเชิงปฏิบัติ-hands-on-examples)
- [เริ่มต้นอย่างรวดเร็ว](#เริ่มต้นอย่างรวดเร็ว)
- [แหล่งข้อมูลเพิ่มเติม](#แหล่งข้อมูลเพิ่มเติม)

### ลิงค์ด่วนไปยังบทเรียน (Quick Links)

**วันที่ 1:**
[บทที่ 1](./day1/01-introduction/README.md) | [บทที่ 2](./day1/02-images/README.md) | [บทที่ 3](./day1/03-containers/README.md) | [บทที่ 4](./day1/04-volumes/README.md) | [บทที่ 5](./day1/05-networks/README.md)

**วันที่ 2:**
[บทที่ 1](./day2/01-dockerfile-best-practices/README.md) | [บทที่ 2](./day2/02-docker-compose/README.md) | [บทที่ 3](./day2/03-real-world-apps/README.md) | [บทที่ 4](./day2/04-best-practices/README.md) | [บทที่ 5](./day2/05-troubleshooting/README.md)

**ตัวอย่าง:**
[Simple Web](./examples/simple-web/README.md) | [Node.js](./examples/node-app/README.md) | [Python Flask](./examples/python-app/README.md)

**แหล่งข้อมูล:**
[Docker Cheat Sheet](./resources/docker-cheatsheet.md) | [สรุปคอร์ส](./COURSE_SUMMARY.md)

---

ยินดีต้อนรับสู่คอร์สเรียน Docker พื้นฐานสำหรับนักพัฒนา 2 วัน! Repository นี้มีเนื้อหาการเรียนรู้ ตัวอย่างโค้ด และแบบฝึกหัดทั้งหมดสำหรับการเรียนรู้พื้นฐาน Docker

## ภาพรวมคอร์ส

คอร์สนี้เป็นคอร์สเชิงปฏิบัติ 2 วันที่ออกแบบมาเพื่อสอนนักพัฒนาเกี่ยวกับพื้นฐาน Docker และการทำ Containerization เมื่อจบคอร์สแล้ว คุณจะสามารถ:

- เข้าใจแนวคิดและสถาปัตยกรรมของ Docker
- สร้างและจัดการ Docker images
- รันและจัดการ Docker containers
- ทำงานกับ Docker volumes และ networks
- ใช้ Docker Compose สำหรับแอปพลิเคชันหลาย container
- ประยุกต์ใช้ best practices ของ Docker

## สิ่งที่ต้องมีก่อนเรียน

- ความเข้าใจพื้นฐานของ Linux command line
- ความคุ้นเคยกับแนวคิดการพัฒนาซอฟต์แวร์
- คอมพิวเตอร์ที่ติดตั้ง Docker แล้ว

## การติดตั้ง Docker

### ขั้นตอนที่ 1: ติดตั้ง Docker Desktop (Windows/Mac)
ดาวน์โหลดและติดตั้ง Docker Desktop จาก: https://www.docker.com/products/docker-desktop

### ขั้นตอนที่ 2: ติดตั้ง Docker Engine (Linux)
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### ขั้นตอนที่ 3: ตรวจสอบการติดตั้ง
```bash
docker --version
docker run hello-world
```

## โครงสร้างคอร์ส

### วันที่ 1: Docker พื้นฐาน

#### บทที่ 1: [แนะนำ Docker](./day1/01-introduction/README.md) 📚
เรียนรู้พื้นฐานของ Docker และทำความเข้าใจว่าทำไมต้องใช้ containerization

**สิ่งที่จะได้เรียนรู้:**
- ขั้นที่ 1: ทำความเข้าใจว่า Docker คืออะไรและประโยชน์ของการใช้ containerization
- ขั้นที่ 2: เปรียบเทียบ Docker กับ Virtual Machines อย่างละเอียด
- ขั้นที่ 3: ศึกษาสถาปัตยกรรมและส่วนประกอบหลักของ Docker (Docker Engine, Docker Daemon, Docker CLI)
- ขั้นที่ 4: ทำความเข้าใจ Docker ecosystem และเครื่องมือที่เกี่ยวข้อง

[👉 เริ่มเรียนบทที่ 1](./day1/01-introduction/README.md)

#### บทที่ 2: [Docker Images](./day1/02-images/README.md) 🖼️
เรียนรู้การสร้างและจัดการ Docker images ซึ่งเป็นพื้นฐานของ containers

**สิ่งที่จะได้เรียนรู้:**
- ขั้นที่ 1: ทำความเข้าใจ Docker images และ image layers
- ขั้นที่ 2: ทำงานกับ Docker Hub และ container registries
- ขั้นที่ 3: สร้าง Dockerfile แรกของคุณและเรียนรู้คำสั่ง Dockerfile พื้นฐาน
- ขั้นที่ 4: Build และ tag images อย่างมีประสิทธิภาพ
- ขั้นที่ 5: เข้าใจการทำงานของ image caching และ layer optimization

[👉 เริ่มเรียนบทที่ 2](./day1/02-images/README.md)

#### บทที่ 3: [Docker Containers](./day1/03-containers/README.md) 📦
เรียนรู้การรันและจัดการ containers ในแบบต่างๆ

**สิ่งที่จะได้เรียนรู้:**
- ขั้นที่ 1: รัน containers ทั้งแบบ interactive และ detached mode
- ขั้นที่ 2: เรียนรู้ lifecycle ของ container (create, start, stop, restart, remove)
- ขั้นที่ 3: จัดการ containers ด้วยคำสั่งต่างๆ และทำ port mapping
- ขั้นที่ 4: ดู logs และ debug containers อย่างมีประสิทธิภาพ
- ขั้นที่ 5: ใช้งาน environment variables และ resource limits

[👉 เริ่มเรียนบทที่ 3](./day1/03-containers/README.md)

#### บทที่ 4: [Docker Volumes](./day1/04-volumes/README.md) 💾
เรียนรู้การจัดการข้อมูลถาวรและการแชร์ข้อมูลระหว่าง containers

**สิ่งที่จะได้เรียนรู้:**
- ขั้นที่ 1: ทำความเข้าใจการเก็บข้อมูลถาวรใน Docker และปัญหาของข้อมูลใน containers
- ขั้นที่ 2: ศึกษาประเภทของ volumes (named volumes, anonymous volumes, bind mounts)
- ขั้นที่ 3: สร้างและจัดการ volumes อย่างมีประสิทธิภาพ
- ขั้นที่ 4: แชร์ข้อมูลระหว่าง containers และ backup/restore ข้อมูล

[👉 เริ่มเรียนบทที่ 4](./day1/04-volumes/README.md)

#### บทที่ 5: [Docker Networks](./day1/05-networks/README.md) 🌐
เรียนรู้การตั้งค่าและจัดการเครือข่ายระหว่าง containers

**สิ่งที่จะได้เรียนรู้:**
- ขั้นที่ 1: เรียนรู้พื้นฐาน container networking และ network drivers
- ขั้นที่ 2: ศึกษาประเภทของ network (bridge, host, none, overlay)
- ขั้นที่ 3: สร้าง user-defined networks และทำให้ containers สื่อสารกัน
- ขั้นที่ 4: เข้าใจ DNS resolution และ network isolation

[👉 เริ่มเรียนบทที่ 5](./day1/05-networks/README.md)

---

### วันที่ 2: Docker ขั้นสูง

#### บทที่ 1: [Dockerfile Best Practices](./day2/01-dockerfile-best-practices/README.md) ⚡
เรียนรู้เทคนิคการเขียน Dockerfile ที่มีประสิทธิภาพและปลอดภัย

**สิ่งที่จะได้เรียนรู้:**
- ขั้นที่ 1: เรียนรู้ multi-stage builds เพื่อลดขนาด image
- ขั้นที่ 2: ปรับปรุง layer optimization และการใช้ cache อย่างมีประสิทธิภาพ
- ขั้นที่ 3: คำนึงถึงด้านความปลอดภัย (security scanning, non-root users)
- ขั้นที่ 4: เลือก base images ที่เหมาะสมและใช้ .dockerignore

[👉 เริ่มเรียนบทที่ 1](./day2/01-dockerfile-best-practices/README.md)

#### บทที่ 2: [Docker Compose](./day2/02-docker-compose/README.md) 🎼
เรียนรู้การจัดการแอปพลิเคชันหลาย containers ด้วย Docker Compose

**สิ่งที่จะได้เรียนรู้:**
- ขั้นที่ 1: แนะนำ Docker Compose และประโยชน์ของการใช้งาน
- ขั้นที่ 2: เรียนรู้ YAML syntax และโครงสร้างไฟล์ docker-compose.yml
- ขั้นที่ 3: สร้างและจัดการแอปพลิเคชันหลาย containers
- ขั้นที่ 4: จัดการ service orchestration, volumes และ networks ใน Compose
- ขั้นที่ 5: ใช้ environment variables และแยก config สำหรับ development/production

[👉 เริ่มเรียนบทที่ 2](./day2/02-docker-compose/README.md)

#### บทที่ 3: [แอปพลิเคชันจริง](./day2/03-real-world-apps/README.md) 🚀
ประยุกต์ใช้ความรู้กับโปรเจกต์จริงและ microservices

**สิ่งที่จะได้เรียนรู้:**
- ขั้นที่ 1: สร้าง web application พร้อม database (full-stack development)
- ขั้นที่ 2: ศึกษาตัวอย่าง microservices architecture
- ขั้นที่ 3: เรียนรู้ development workflow และ CI/CD integration
- ขั้นที่ 4: จัดการกับ multi-tier applications

[👉 เริ่มเรียนบทที่ 3](./day2/03-real-world-apps/README.md)

#### บทที่ 4: [Docker Best Practices](./day2/04-best-practices/README.md) ⭐
เรียนรู้ best practices สำหรับการใช้งาน Docker ใน production

**สิ่งที่จะได้เรียนรู้:**
- ขั้นที่ 1: ปรับปรุง image ให้มีประสิทธิภาพและมีขนาดเล็ก
- ขั้นที่ 2: ใช้ security best practices (vulnerability scanning, secrets management)
- ขั้นที่ 3: พิจารณาเรื่อง resource management และ monitoring สำหรับ production
- ขั้นที่ 4: เรียนรู้ deployment strategies และ health checks

[👉 เริ่มเรียนบทที่ 4](./day2/04-best-practices/README.md)

#### บทที่ 5: [การแก้ปัญหา](./day2/05-troubleshooting/README.md) 🔧
เรียนรู้วิธีแก้ปัญหาและ debug Docker อย่างมีประสิทธิภาพ

**สิ่งที่จะได้เรียนรู้:**
- ขั้นที่ 1: เรียนรู้ปัญหาทั่วไปและวิธีแก้ไขอย่างเป็นระบบ
- ขั้นที่ 2: เทคนิคการ debug containers และ images
- ขั้นที่ 3: แก้ไขปัญหา networking และ volumes
- ขั้นที่ 4: ปรับปรุงประสิทธิภาพและ troubleshooting performance issues

[👉 เริ่มเรียนบทที่ 5](./day2/05-troubleshooting/README.md)

## ตัวอย่างเชิงปฏิบัติ (Hands-on Examples)

เรียนรู้จากตัวอย่างโปรเจกต์จริงที่พร้อมใช้งาน:

### 1. [Simple Web - เว็บไซต์ HTML พื้นฐาน](./examples/simple-web/README.md) 🌐
ตัวอย่าง containerization เว็บไซต์แบบคงที่ด้วย Nginx
- เรียนรู้การสร้าง Dockerfile พื้นฐาน
- ทำความเข้าใจ port mapping และการให้บริการไฟล์แบบ static
- เหมาะสำหรับผู้เริ่มต้น

[👉 ดูตัวอย่าง Simple Web](./examples/simple-web/README.md)

### 2. [Node.js Application](./examples/node-app/README.md) 🟢
ตัวอย่าง REST API ด้วย Express.js framework
- เรียนรู้ multi-stage builds สำหรับ Node.js
- ทำความเข้าใจการจัดการ dependencies (npm)
- เรียนรู้การตั้งค่า environment variables
- ศึกษา development vs production modes

[👉 ดูตัวอย่าง Node.js App](./examples/node-app/README.md)

### 3. [Python Flask Application](./examples/python-app/README.md) 🐍
ตัวอย่าง web application ด้วย Flask framework
- เรียนรู้ containerization สำหรับแอปพลิเคชัน Python
- ทำความเข้าใจการใช้ requirements.txt
- เรียนรู้การตั้งค่า WSGI server (Gunicorn)
- ศึกษา health checks และ best practices

[👉 ดูตัวอย่าง Python App](./examples/python-app/README.md)

---

## เริ่มต้นอย่างรวดเร็ว

### แบบฝึกหัดวันที่ 1
```bash
cd day1
# ทำตามแบบฝึกหัดในแต่ละ subdirectory
# เริ่มจาก 01-introduction จนถึง 05-networks
```

### แบบฝึกหัดวันที่ 2
```bash
cd day2
# ทำตามแบบฝึกหัดในแต่ละ subdirectory
# เริ่มจาก 01-dockerfile-best-practices จนถึง 05-troubleshooting
```

### ลองตัวอย่างเชิงปฏิบัติ
```bash
cd examples
# เลือกตัวอย่างที่ต้องการลอง
cd simple-web   # หรือ node-app หรือ python-app
# ทำตามคำแนะนำใน README.md ของแต่ละตัวอย่าง
```

## แหล่งข้อมูลเพิ่มเติม

### เอกสารอ้างอิงภายใน Repository
- 📋 [Docker Cheat Sheet](./resources/docker-cheatsheet.md) - คู่มืออ้างอิงคำสั่ง Docker ที่จำเป็นทั้งหมด
- 📚 [สรุปคอร์ส](./COURSE_SUMMARY.md) - ภาพรวมโดยละเอียดของคอร์สทั้งหมด

### เอกสารและแหล่งเรียนรู้ภายนอก
- [เอกสาร Docker อย่างเป็นทางการ](https://docs.docker.com) - เอกสารครบถ้วนจาก Docker
- [Docker Hub](https://hub.docker.com) - คลังเก็บ Docker images สาธารณะ
- [Docker Blog](https://www.docker.com/blog/) - บทความและข่าวสารเกี่ยวกับ Docker
- [Play with Docker](https://labs.play-with-docker.com/) - ทดลองใช้ Docker ออนไลน์ฟรี

## ลิขสิทธิ์

Repository นี้สำหรับวัตถุประสงค์ทางการศึกษา

## การสนับสนุน

หากคุณมีคำถามหรือปัญหา กรุณาเปิด issue ใน repository นี้

---

สนุกกับการเรียนรู้! 🐳