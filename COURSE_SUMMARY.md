# สรุปคอร์สเรียน Docker 2 วัน

## สิ่งที่มีใน Repository นี้

Repository นี้ประกอบด้วยคอร์สเรียน Docker แบบครบถ้วน 2 วัน ออกแบบมาสำหรับนักพัฒนาที่ต้องการเรียนรู้ Docker ตั้งแต่พื้นฐานจนถึงการใช้งานจริง

## โครงสร้าง Repository

```
docker-2days/
├── README.md                          # ภาพรวมคอร์สและการนำทาง
├── COURSE_SUMMARY.md                  # ไฟล์นี้
├── .gitignore                         # การตั้งค่า Git ignore
│
├── day1/                              # วันที่ 1: พื้นฐาน Docker
│   ├── 01-introduction/              # พื้นฐานและสถาปัตยกรรม Docker
│   ├── 02-images/                    # การทำงานกับ Docker images
│   ├── 03-containers/                # การจัดการ container
│   ├── 04-volumes/                   # การเก็บข้อมูลถาวร
│   └── 05-networks/                  # การเชื่อมต่อเครือข่าย container
│
├── day2/                              # วันที่ 2: Docker ขั้นสูง
│   ├── 01-dockerfile-best-practices/ # การปรับปรุง Dockerfiles
│   ├── 02-docker-compose/            # แอปพลิเคชันหลาย containers
│   ├── 03-real-world-apps/           # ตัวอย่างการใช้งานจริง
│   ├── 04-best-practices/            # แนวทางสำหรับ production
│   └── 05-troubleshooting/           # การแก้ไขปัญหาและ debug
│
├── examples/                          # ตัวอย่างโค้ดเชิงปฏิบัติ
│   ├── simple-web/                   # HTML แบบคงที่กับ Nginx
│   ├── node-app/                     # แอปพลิเคชัน Node.js Express
│   └── python-app/                   # แอปพลิเคชัน Python Flask
│
└── resources/                         # เอกสารเพิ่มเติม
    └── docker-cheatsheet.md          # คู่มืออ้างอิงด่วน
```

## เนื้อหาคอร์ส

### วันที่ 1: พื้นฐาน Docker (5 โมดูล)

#### 1. แนะนำ Docker
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: Docker คืออะไรและทำไมต้องใช้
- ขั้นที่ 2: เปรียบเทียบ Docker กับ Virtual Machines
- ขั้นที่ 3: ศึกษาส่วนประกอบสถาปัตยกรรม Docker
- ขั้นที่ 4: เรียนรู้คำสั่ง Docker พื้นฐาน
- ขั้นที่ 5: ฝึกสร้าง container แรก

#### 2. Docker Images
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: ทำความเข้าใจ Docker images
- ขั้นที่ 2: ทำงานกับ Docker Hub
- ขั้นที่ 3: สร้าง Dockerfiles
- ขั้นที่ 4: Build images
- ขั้นที่ 5: เรียนรู้เกี่ยวกับ image layers และ caching
- ขั้นที่ 6: จัดการ images

#### 3. Docker Containers
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: เรียนรู้ lifecycle ของ container
- ขั้นที่ 2: รัน containers (แบบ detached และ interactive)
- ขั้นที่ 3: ทำ port mapping
- ขั้นที่ 4: ใช้คำสั่งจัดการ container
- ขั้นที่ 5: รันคำสั่งภายใน containers
- ขั้นที่ 6: ดู container logs และการ debug
- ขั้นที่ 7: ใช้ environment variables
- ขั้นที่ 8: กำหนด resource limits

#### 4. Docker Volumes
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: ทำความเข้าใจแนวคิดการเก็บข้อมูลถาวร
- ขั้นที่ 2: ศึกษาประเภท volumes (named, anonymous, bind mounts)
- ขั้นที่ 3: สร้างและจัดการ volumes
- ขั้นที่ 4: แชร์ volumes ระหว่าง containers
- ขั้นที่ 5: วิธีการ backup และ restore

#### 5. Docker Networks
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: เรียนรู้พื้นฐาน container networking
- ขั้นที่ 2: ศึกษา network drivers (bridge, host, none)
- ขั้นที่ 3: สร้าง user-defined networks
- ขั้นที่ 4: ทำให้ containers สื่อสารกัน
- ขั้นที่ 5: เรียนรู้ DNS resolution
- ขั้นที่ 6: ใช้ network isolation patterns

### วันที่ 2: Docker ขั้นสูง (5 โมดูล)

#### 1. Dockerfile Best Practices
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: ปรับปรุง layer optimization
- ขั้นที่ 2: เรียนรู้ multi-stage builds
- ขั้นที่ 3: เลือก base images ที่เหมาะสม
- ขั้นที่ 4: ใช้ .dockerignore
- ขั้นที่ 5: รันในฐานะ non-root user
- ขั้นที่ 6: คำนึงถึงความปลอดภัย
- ขั้นที่ 7: ลดขนาด image

#### 2. Docker Compose
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: แนะนำ Docker Compose
- ขั้นที่ 2: เรียนรู้การตั้งค่า YAML
- ขั้นที่ 3: กำหนด service definitions
- ขั้นที่ 4: สร้างแอปพลิเคชันหลาย containers
- ขั้นที่ 5: ใช้ environment variables
- ขั้นที่ 6: จัดการ volumes และ networks ใน Compose
- ขั้นที่ 7: เรียนรู้คำสั่ง Docker Compose
- ขั้นที่ 8: แยก configs สำหรับ Development และ Production

#### 3. แอปพลิเคชันจริง
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: สร้าง MERN Stack (MongoDB, Express, React, Node.js)
- ขั้นที่ 2: สร้าง Django + PostgreSQL + Redis
- ขั้นที่ 3: ศึกษา microservices architecture
- ขั้นที่ 4: ดูตัวอย่างแพลตฟอร์ม e-commerce
- ขั้นที่ 5: เชื่อมต่อกับ CI/CD
- ขั้นที่ 6: เรียนรู้ development workflows

#### 4. Best Practices
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: ใช้ security best practices
- ขั้นที่ 2: เทคนิคการปรับปรุง image
- ขั้นที่ 3: จัดการ resources
- ขั้นที่ 4: กลยุทธ์ networking
- ขั้นที่ 5: รูปแบบการเก็บข้อมูลถาวร
- ขั้นที่ 6: ตั้งค่า environment configuration
- ขั้นที่ 7: การ monitoring และ logging
- ขั้นที่ 8: checklist สำหรับ production

#### 5. การแก้ปัญหา
**ขั้นตอนการเรียนรู้:**
- ขั้นที่ 1: ปัญหาทั่วไปและวิธีแก้ไข
- ขั้นที่ 2: แก้ปัญหาการ startup ของ container
- ขั้นที่ 3: debug network
- ขั้นที่ 4: แก้ปัญหา volume และ permissions
- ขั้นที่ 5: แก้ไข image build failures
- ขั้นที่ 6: แก้ปัญหาประสิทธิภาพ
- ขั้นที่ 7: เทคนิคการ debugging
- ขั้นที่ 8: ขั้นตอนการ recovery

## ตัวอย่างเชิงปฏิบัติ

### 1. เว็บไซต์แบบง่าย (HTML + Nginx)
เว็บไซต์แบบคงที่พื้นฐานที่ให้บริการด้วย Nginx แสดงให้เห็น:
**ขั้นตอน:**
- ขั้นที่ 1: สร้าง Dockerfile พื้นฐาน
- ขั้นที่ 2: Build และรัน containers
- ขั้นที่ 3: ทำ port mapping
- ขั้นที่ 4: Mount volumes

### 2. แอปพลิเคชัน Node.js
แอปพลิเคชัน API ด้วย Express.js แสดงให้เห็น:
**ขั้นตอน:**
- ขั้นที่ 1: รูปแบบ Dockerfile สำหรับ Node.js
- ขั้นที่ 2: Multi-stage builds
- ขั้นที่ 3: ตั้งค่า health checks
- ขั้นที่ 4: ตั้งค่า non-root user
- ขั้นที่ 5: แยกโหมด development และ production

### 3. แอปพลิเคชัน Python Flask
REST API ด้วย Flask แสดงให้เห็น:
**ขั้นตอน:**
- ขั้นที่ 1: containerization สำหรับแอปพลิเคชัน Python
- ขั้นที่ 2: ใช้ Gunicorn สำหรับ production
- ขั้นที่ 3: จัดการ virtual environment
- ขั้นที่ 4: ตั้งค่า health check endpoints
- ขั้นที่ 5: ใช้ security best practices

## แหล่งข้อมูล

### Docker Cheat Sheet
คู่มืออ้างอิงด่วนที่ครอบคลุม:
- คำสั่ง Docker ที่จำเป็นทั้งหมด
- คำสั่ง Dockerfile
- ไวยากรณ์ Docker Compose
- รูปแบบทั่วไปและการแก้ปัญหา
- เตือนความจำ best practices

## เส้นทางการเรียนรู้

### สำหรับผู้เริ่มต้น
**ทำตามขั้นตอนเหล่านี้:**
- ขั้นที่ 1: เริ่มจาก README.md เพื่อดูภาพรวมคอร์ส
- ขั้นที่ 2: ทำตามโมดูลวันที่ 1 ตามลำดับ (01 → 05)
- ขั้นที่ 3: ลองตัวอย่างใน directory `examples/`
- ขั้นที่ 4: ทำโมดูลวันที่ 2 ตามลำดับ
- ขั้นที่ 5: ใช้ cheat sheet เป็นเอกสารอ้างอิงตามต้องการ

### สำหรับผู้ใช้ระดับกลาง
**ทำตามขั้นตอนเหล่านี้:**
- ขั้นที่ 1: ทบทวนโมดูลวันที่ 1 อย่างรวดเร็ว
- ขั้นที่ 2: เน้นหัวข้อขั้นสูงในวันที่ 2
- ขั้นที่ 3: ศึกษาตัวอย่างแอปพลิเคชันจริง
- ขั้นที่ 4: นำ best practices ไปใช้ในโปรเจกต์ของคุณ
- ขั้นที่ 5: ใช้คู่มือการแก้ปัญหาเป็นเอกสารอ้างอิง

### สำหรับการฝึกปฏิบัติ
**ทำตามขั้นตอนเหล่านี้:**
- ขั้นที่ 1: แต่ละโมดูลมีแบบฝึกหัดเชิงปฏิบัติ
- ขั้นที่ 2: มีตัวอย่างที่ใช้งานได้จริงสามตัวอย่าง
- ขั้นที่ 3: สามารถขยายและแก้ไขเพื่อการเรียนรู้
- ขั้นที่ 4: ตัวอย่างใช้ tech stacks ที่นิยม

## ผลลัพธ์การเรียนรู้หลัก

หลังจบคอร์สนี้ ผู้เรียนจะสามารถ:

✅ เข้าใจแนวคิดและสถาปัตยกรรมของ Docker
✅ สร้าง Docker images ที่มีประสิทธิภาพ
✅ รันและจัดการ containers อย่างมีประสิทธิผล
✅ ใช้กลยุทธ์การเก็บข้อมูลถาวร
✅ ตั้งค่า container networking
✅ ใช้ Docker Compose สำหรับแอปพลิเคชันหลาย containers
✅ ใช้ security best practices
✅ แก้ปัญหา Docker ทั่วไป
✅ Deploy แอปพลิเคชันที่พร้อมสำหรับ production
✅ ทำตาม industry best practices

## คุณสมบัติของคอร์ส

- **ครอบคลุม**: ครอบคลุมตั้งแต่พื้นฐานจนถึงหัวข้อขั้นสูง
- **เชิงปฏิบัติ**: แบบฝึกหัดเชิงปฏิบัติในทุกโมดูล
- **โลกจริง**: ตัวอย่างที่พร้อมสำหรับ production
- **โครงสร้างดี**: เส้นทางการเรียนรู้แบบก้าวหน้า
- **เอกสารอ้างอิง**: cheat sheet อ้างอิงด่วน
- **Best practices**: แนวทางความปลอดภัยและการปรับปรุง
- **การแก้ปัญหา**: ปัญหาทั่วไปและวิธีแก้ไข

## Tech Stack ที่ครอบคลุม

- **ภาษา**: Node.js, Python, HTML/CSS
- **Frameworks**: Express.js, Flask
- **Databases**: PostgreSQL, MongoDB, MySQL, Redis
- **Web Servers**: Nginx
- **เครื่องมือ**: Docker, Docker Compose
- **แพลตฟอร์ม**: Linux, macOS, Windows

## ความรู้พื้นฐานที่แนะนำ

- ความรู้พื้นฐาน command line
- ความคุ้นเคยกับภาษาโปรแกรมมิ่งอย่างน้อยหนึ่งภาษา
- ความเข้าใจแนวคิดของ web application
- ความเข้าใจพื้นฐานเกี่ยวกับ networking (เป็นประโยชน์แต่ไม่จำเป็น)

## ระยะเวลาคอร์ส

- **วันที่ 1**: 6-8 ชั่วโมง (รวมแบบฝึกหัดเชิงปฏิบัติ)
- **วันที่ 2**: 6-8 ชั่วโมง (รวมแบบฝึกหัดเชิงปฏิบัติ)
- **รวม**: 12-16 ชั่วโมงของการฝึกอบรมที่ครอบคลุม

## ลิขสิทธิ์

Repository นี้สำหรับวัตถุประสงค์ทางการศึกษา

---

**สนุกกับการเรียนรู้! 🐳**

เริ่มต้นการเดินทาง Docker ของคุณโดยเปิดไฟล์ [README.md](README.md)!
