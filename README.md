# คอร์สเรียน Docker 2 วัน

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

#### บทที่ 1: แนะนำ Docker (`day1/01-introduction/`)
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: ทำความเข้าใจว่า Docker คืออะไร
- ขั้นที่ 2: เปรียบเทียบ Docker กับ Virtual Machines
- ขั้นที่ 3: ศึกษาสถาปัตยกรรมและส่วนประกอบของ Docker

#### บทที่ 2: Docker Images (`day1/02-images/`)
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: ทำความเข้าใจ Docker images
- ขั้นที่ 2: ทำงานกับ Docker Hub
- ขั้นที่ 3: สร้าง Dockerfile แรกของคุณ
- ขั้นที่ 4: Build images

#### บทที่ 3: Docker Containers (`day1/03-containers/`)
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: รัน containers
- ขั้นที่ 2: เรียนรู้ lifecycle ของ container
- ขั้นที่ 3: จัดการ containers
- ขั้นที่ 4: ดู logs และ debug containers

#### บทที่ 4: Docker Volumes (`day1/04-volumes/`)
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: ทำความเข้าใจการเก็บข้อมูลถาวรใน Docker
- ขั้นที่ 2: ศึกษาประเภทและการจัดการ volumes
- ขั้นที่ 3: เปรียบเทียบ bind mounts กับ volumes

#### บทที่ 5: Docker Networks (`day1/05-networks/`)
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: เรียนรู้พื้นฐาน container networking
- ขั้นที่ 2: ศึกษาประเภทของ network
- ขั้นที่ 3: ทำให้ containers สื่อสารกันได้

### วันที่ 2: Docker ขั้นสูง

#### บทที่ 1: Dockerfile Best Practices (`day2/01-dockerfile-best-practices/`)
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: เรียนรู้ multi-stage builds
- ขั้นที่ 2: ปรับปรุง layer optimization
- ขั้นที่ 3: คำนึงถึงด้านความปลอดภัย

#### บทที่ 2: Docker Compose (`day2/02-docker-compose/`)
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: แนะนำ Docker Compose
- ขั้นที่ 2: เรียนรู้ YAML syntax
- ขั้นที่ 3: สร้างแอปพลิเคชันหลาย containers
- ขั้นที่ 4: จัดการ service orchestration

#### บทที่ 3: แอปพลิเคชันจริง (`day2/03-real-world-apps/`)
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: สร้าง web application พร้อม database
- ขั้นที่ 2: ศึกษาตัวอย่าง microservices
- ขั้นที่ 3: เรียนรู้ development workflow

#### บทที่ 4: Docker Best Practices (`day2/04-best-practices/`)
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: ปรับปรุง image ให้มีประสิทธิภาพ
- ขั้นที่ 2: ใช้ security best practices
- ขั้นที่ 3: พิจารณาสำหรับ production

#### บทที่ 5: การแก้ปัญหา (`day2/05-troubleshooting/`)
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: เรียนรู้ปัญหาทั่วไปและวิธีแก้ไข
- ขั้นที่ 2: เทคนิคการ debug
- ขั้นที่ 3: ปรับปรุงประสิทธิภาพ

## เริ่มต้นอย่างรวดเร็ว

### แบบฝึกหัดวันที่ 1
```bash
cd day1
# ทำตามแบบฝึกหัดในแต่ละ subdirectory
```

### แบบฝึกหัดวันที่ 2
```bash
cd day2
# ทำตามแบบฝึกหัดในแต่ละ subdirectory
```

## แหล่งข้อมูลเพิ่มเติม

- เอกสาร Docker อย่างเป็นทางการ: https://docs.docker.com
- Docker Hub: https://hub.docker.com
- Docker Cheat Sheet: `./resources/docker-cheatsheet.md`

## ลิขสิทธิ์

Repository นี้สำหรับวัตถุประสงค์ทางการศึกษา

## การสนับสนุน

หากคุณมีคำถามหรือปัญหา กรุณาเปิด issue ใน repository นี้

---

สนุกกับการเรียนรู้! 🐳