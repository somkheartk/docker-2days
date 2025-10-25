# วันที่ 1 - Docker Networks

## Docker Networking คืออะไร?

Docker networking ช่วยให้ containers สามารถสื่อสารกันได้และกับระบบภายนอก โดยค่าเริ่มต้น containers จะแยกออกจากกัน

## ประเภทของ Network Drivers

### 1. Bridge (ค่าเริ่มต้น)
- Network driver เริ่มต้น
- ใช้สำหรับ containers บนเครื่อง host เดียวกัน
- Containers สามารถสื่อสารกันผ่าน IP addresses

### 2. Host
- ลบการแยก network ระหว่าง container และ host
- Container ใช้ network stack ของ host โดยตรง
- ประสิทธิภาพสูงกว่า แต่มีการแยกน้อยกว่า

### 3. None
- ปิดการใช้งาน networking
- Container จะแยกอย่างสมบูรณ์

### 4. Overlay
- สำหรับ multi-host networking
- ใช้กับ Docker Swarm

### 5. Macvlan
- กำหนด MAC address ให้กับ container
- Container ปรากฏเป็นอุปกรณ์ทางกายภาพบน network

## การทำงานกับ Networks

### ขั้นตอนที่ 1: แสดงรายการ Networks
```bash
docker network ls
```

### ขั้นตอนที่ 2: ตรวจสอบ Network
```bash
docker network inspect bridge
```

### ขั้นตอนที่ 3: สร้าง Network
```bash
docker network create my-network
docker network create --driver bridge custom-bridge
```

### ขั้นตอนที่ 4: ลบ Network
```bash
docker network rm my-network
docker network prune  # ลบ networks ที่ไม่ได้ใช้
```

## Default Bridge Network

### ข้อจำกัด:
- Containers ต้องใช้ IP addresses ในการสื่อสาร
- ไม่มี automatic DNS resolution
- ต้อง link containers ด้วยตนเอง

### ตัวอย่าง:
```bash
docker run -d --name web1 nginx
docker run -d --name web2 nginx

# ต้องใช้ IP address
docker exec web1 ping <IP-of-web2>
```

## User-Defined Bridge Networks (แนะนำ)

### ประโยชน์:
- Automatic DNS resolution
- Better isolation
- Containers สามารถเชื่อมต่อและถูกตัดการเชื่อมต่อได้อย่างยืดหยุ่น
- การตั้งค่า configuration ที่ดีกว่า

## แบบฝึกหัดที่ 1: สร้าง Custom Network

### ขั้นตอนที่ 1: สร้าง network
```bash
docker network create app-network
```

### ขั้นตอนที่ 2: รัน containers บน network
```bash
docker run -d --name web --network app-network nginx
docker run -d --name api --network app-network alpine sleep 3600
```

### ขั้นตอนที่ 3: ทดสอบการเชื่อมต่อโดยใช้ชื่อ
```bash
docker exec api ping web
docker exec web ping api
```

### ขั้นตอนที่ 4: ตรวจสอบ network
```bash
docker network inspect app-network
```

## แบบฝึกหัดที่ 2: Multi-Container Application

### ขั้นตอนที่ 1: สร้าง network
```bash
docker network create wordpress-net
```

### ขั้นตอนที่ 2: รัน MySQL
```bash
docker run -d \
  --name mysql \
  --network wordpress-net \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=wordpress \
  mysql:8
```

### ขั้นตอนที่ 3: รัน WordPress
```bash
docker run -d \
  --name wordpress \
  --network wordpress-net \
  -p 8080:80 \
  -e WORDPRESS_DB_HOST=mysql \
  -e WORDPRESS_DB_PASSWORD=secret \
  wordpress
```

### ขั้นตอนที่ 4: เข้าถึง WordPress
เปิดเบราว์เซอร์ไปที่: http://localhost:8080

### ขั้นตอนที่ 5: ตรวจสอบการเชื่อมต่อ
```bash
docker exec wordpress ping mysql
```

## เชื่อมต่อ Container กับหลาย Networks

### ขั้นตอนที่ 1: สร้าง networks
```bash
docker network create frontend
docker network create backend
```

### ขั้นตอนที่ 2: รัน database บน backend
```bash
docker run -d --name database --network backend mysql:8
```

### ขั้นตอนที่ 3: รัน API บนทั้ง frontend และ backend
```bash
docker run -d --name api --network backend nginx
docker network connect frontend api
```

### ขั้นตอนที่ 4: รัน web frontend
```bash
docker run -d --name web --network frontend nginx
```

ตอนนี้:
- `web` สามารถเข้าถึง `api` ได้
- `api` สามารถเข้าถึง `database` ได้
- `web` ไม่สามารถเข้าถึง `database` ได้โดยตรง (การแยก)

## Host Network

### ขั้นตอนที่ 1: รัน container ด้วย host network
```bash
docker run -d --name host-nginx --network host nginx
```

**หมายเหตุ**: Container จะใช้ port 80 ของ host โดยตรง ไม่ต้องทำ port mapping

### ข้อควรพิจารณา:
- ประสิทธิภาพสูงกว่า
- ไม่มี network isolation
- Port conflicts เป็นไปได้
- ทำงานได้ดีที่สุดบน Linux

## แบบฝึกหัดที่ 3: Network Aliases

### ขั้นตอนที่ 1: สร้าง network
```bash
docker network create test-net
```

### ขั้นตอนที่ 2: รัน containers ด้วย aliases
```bash
docker run -d --name web1 --network test-net --network-alias web nginx
docker run -d --name web2 --network test-net --network-alias web nginx
docker run -d --name web3 --network test-net --network-alias web nginx
```

### ขั้นตอนที่ 3: ทดสอบ load balancing
```bash
docker run --rm --network test-net alpine sh -c "for i in 1 2 3 4 5; do wget -qO- web; done"
```

Requests จะถูกกระจายไปยัง containers ต่างๆ

## Port Publishing

### แมป port เฉพาะ
```bash
docker run -d -p 8080:80 nginx
```

### แมป port หลายตัว
```bash
docker run -d -p 8080:80 -p 8443:443 nginx
```

### แมปไปยัง host IP เฉพาะ
```bash
docker run -d -p 127.0.0.1:8080:80 nginx
```

### ให้ Docker เลือก host port
```bash
docker run -d -p 80 nginx
docker port <container-name>
```

### แมป port range
```bash
docker run -d -p 8080-8090:8080-8090 nginx
```

## แบบฝึกหัดที่ 4: Container Communication

### ขั้นตอนที่ 1: สร้าง network และ containers
```bash
docker network create demo-net

# Backend API
docker run -d --name api --network demo-net \
  alpine sh -c "while true; do nc -l -p 3000 -e echo 'API Response'; done"

# Frontend
docker run -d --name frontend --network demo-net \
  -p 8080:80 nginx
```

### ขั้นตอนที่ 2: ทดสอบการสื่อสาร
```bash
docker exec frontend ping api
docker exec frontend nc api 3000
```

## DNS Resolution

ใน user-defined networks:
- Containers สามารถ resolve กันได้โดยชื่อ
- Docker ให้บริการ embedded DNS server
- ทำงานโดยอัตโนมัติ

### ตัวอย่าง:
```bash
docker network create my-net
docker run -d --name server1 --network my-net alpine sleep 3600
docker run -d --name server2 --network my-net alpine sleep 3600

# DNS resolution
docker exec server1 nslookup server2
docker exec server1 ping server2
```

## แบบฝึกหัดที่ 5: Nginx Reverse Proxy

### ขั้นตอนที่ 1: สร้าง network
```bash
docker network create proxy-net
```

### ขั้นตอนที่ 2: รัน backend services
```bash
docker run -d --name app1 --network proxy-net nginx
docker run -d --name app2 --network proxy-net nginx
```

### ขั้นตอนที่ 3: สร้าง nginx config
```bash
cat > nginx.conf << EOF
events {}
http {
    upstream backend {
        server app1:80;
        server app2:80;
    }
    server {
        listen 80;
        location / {
            proxy_pass http://backend;
        }
    }
}
EOF
```

### ขั้นตอนที่ 4: รัน reverse proxy
```bash
docker run -d --name proxy \
  --network proxy-net \
  -p 8080:80 \
  -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
  nginx
```

### ขั้นตอนที่ 5: ทดสอบ load balancing
```bash
curl http://localhost:8080
```

## Network Troubleshooting

### ตรวจสอบ network configuration
```bash
docker network inspect <network-name>
```

### ดู containers ใน network
```bash
docker network inspect <network-name> --format='{{range .Containers}}{{.Name}} {{end}}'
```

### ทดสอบการเชื่อมต่อ
```bash
# Ping
docker exec <container> ping <target>

# Telnet
docker exec <container> telnet <host> <port>

# Curl
docker exec <container> curl <url>

# DNS lookup
docker exec <container> nslookup <hostname>
```

### ตรวจสอบ ports
```bash
docker port <container-name>
```

## แบบฝึกหัดที่ 6: Network Isolation

### ขั้นตอนที่ 1: สร้าง isolated networks
```bash
docker network create net-a
docker network create net-b
```

### ขั้นตอนที่ 2: รัน containers
```bash
docker run -d --name container-a --network net-a alpine sleep 3600
docker run -d --name container-b --network net-b alpine sleep 3600
```

### ขั้นตอนที่ 3: ทดสอบ isolation
```bash
# นี่จะล้มเหลว - ไม่มีการเชื่อมต่อ
docker exec container-a ping container-b
```

### ขั้นตอนที่ 4: เชื่อมต่อ networks
```bash
docker network connect net-b container-a
# ตอนนี้ container-a อยู่ในทั้ง net-a และ net-b
docker exec container-a ping container-b
```

## Best Practices

1. **ใช้ User-Defined Networks**: ไม่ใช่ default bridge
2. **ตั้งชื่อที่มีความหมาย**: networks และ containers
3. **แยก Concerns**: frontend, backend, database networks
4. **ใช้ Network Aliases**: สำหรับ load balancing
5. **จำกัด Port Exposure**: เปิดเฉพาะ ports ที่จำเป็น
6. **Monitor Network Traffic**: ใช้เครื่องมือ monitoring
7. **Document Network Architecture**: สำหรับทีม
8. **ใช้ DNS Names**: ไม่ใช่ IP addresses
9. **ทำความสะอาดเป็นประจำ**: ลบ networks ที่ไม่ได้ใช้
10. **Test Connectivity**: ตรวจสอบการเชื่อมต่อระหว่าง services

## Network Security

### เคล็ดลับความปลอดภัย:
1. ใช้ user-defined networks สำหรับ isolation
2. จำกัด port exposure
3. ใช้ network policies (ใน Swarm/Kubernetes)
4. Encrypt traffic ระหว่าง containers
5. Monitor network access
6. ใช้ firewall rules
7. แยก sensitive data บน isolated networks
8. Regular security audits

## ข้อมูลเพิ่มเติม

### ดู network drivers ที่มี
```bash
docker network ls --format "{{.Driver}}"
```

### สร้าง network พร้อม options เพิ่มเติม
```bash
docker network create --driver bridge \
  --subnet=172.20.0.0/16 \
  --ip-range=172.20.240.0/20 \
  --gateway=172.20.0.1 \
  custom-network
```

### เชื่อมต่อ container กับ network ด้วย specific IP
```bash
docker network connect --ip 172.20.0.10 custom-network my-container
```

## ขั้นตอนถัดไป

ยินดีด้วย! คุณได้เรียนจบพื้นฐาน Docker ของวันที่ 1 แล้ว  
ไปต่อที่ [Day 2](../../day2/01-dockerfile-best-practices/README.md) เพื่อเรียนรู้เทคนิคขั้นสูง
