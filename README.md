# 🤖 ROS2Go AMR API

REST API แบบ **Modular** สำหรับควบคุมหุ่นยนต์ **ROS 2 Autonomous Mobile Robot (AMR)** พัฒนาด้วย **FastAPI** เพื่อให้สามารถเชื่อมต่อกับ Web UI และ Dashboard ได้อย่างมีประสิทธิภาพ รองรับการจัดการวงจรชีวิตของหุ่นยนต์ การควบคุมระบบ และการตรวจสอบสถานะแบบเรียลไทม์

---
## 🎛 PORT: 8000
---
# 📂 ตำแหน่งติดตั้ง
/opt/ros2go/api
---
# ✨ Features

- **Process Management**
  - สั่งเริ่มและหยุดโหมดการทำงาน เช่น Bringup, Mapping และ Navigation ได้แบบไดนามิก

- **System Monitoring**
  - ตรวจสอบสถานะ CPU, RAM, Battery, Uptime และ Hardware Serial Number แบบเรียลไทม์

- **Map Management**
  - บันทึกแผนที่จาก SLAM
  - แสดงรายการไฟล์แผนที่ที่มีอยู่ในระบบ

- **Safety System**
  - รองรับ Software Emergency Stop (E-Stop)
  - ส่งคำสั่งความเร็วเป็น `0` ไปยัง `/cmd_vel` ทันที

- **Power Management**
  - รีบูต (Reboot)
  - ปิดเครื่อง (Power Off)
  - มีระบบป้องกันการปิดเครื่องขณะหุ่นยนต์กำลังทำงาน

- **Authentication & License**
  - ป้องกัน API ด้วย `X-API-Key`
  - รองรับระบบ License Key ที่ผูกกับ Hardware

---

# 📂 Project Structure

```text
ros2go_amr_api/
├── main.py               # Entry point และรวม Router ทั้งหมด
├── config.py             # Configuration และ Constants
├── state.py              # Global State (แก้ปัญหา Circular Import)
├── auth.py               # API Authentication
├── ros2/
│   ├── __init__.py
│   └── node.py           # ROS2 Publisher / Subscriber
└── routers/
    ├── __init__.py
    ├── system.py         # System Info / Power / License
    ├── process.py        # Launch / Stop Process
    ├── safety.py         # Emergency Stop
    └── map.py            # Map Management
```

---

# 🛠️ System Requirements

- Ubuntu / Debian
- ROS 2 Jazzy (หรือเวอร์ชันที่รองรับ)
- Python 3

---

# 📦 Installation

## 1. ติดตั้ง Python Packages

```bash
pip3 install fastapi uvicorn pydantic
```

---

## 2. สร้างโฟลเดอร์ที่จำเป็น

```bash
sudo mkdir -p /opt/ros2go/maps
sudo mkdir -p /opt/ros2go/license
```

เปลี่ยนสิทธิ์ให้เป็นผู้ใช้งานปัจจุบัน

```bash
sudo chown -R $USER:$USER /opt/ros2go/maps
sudo chown -R $USER:$USER /opt/ros2go/license
```

---

## 3. อนุญาตให้ Reboot / Poweroff โดยไม่ต้องใส่รหัสผ่าน (แนะนำ)

เปิดไฟล์ sudoers

```bash
sudo visudo
```

เพิ่มบรรทัดนี้ (เปลี่ยน `ubuntu` ให้เป็น Username ของเครื่อง)

```text
ubuntu ALL=(ALL) NOPASSWD: /usr/sbin/reboot, /usr/sbin/poweroff
```

---

# 🚀 Running the API

โหลด ROS Environment

```bash
source /opt/ros/jazzy/setup.bash
```

รันเซิร์ฟเวอร์

```bash
python3 main.py
```

API จะทำงานที่

```
http://0.0.0.0:8000
```

---

# 🔐 Authentication

ทุก Endpoint ภายใต้

```
/api/v1/*
```

จำเป็นต้องส่ง HTTP Header

| Header | Value |
|---------|-------|
| X-API-Key | Your API Key |

ค่าเริ่มต้น

```text
MT-Robotics-AMR-Secret-Key-2026
```

> **แนะนำ:** ควรเปลี่ยน API Key ใน `config.py` ก่อนนำไปใช้งานจริง

ตัวอย่าง

```bash
curl -X GET http://localhost:8000/api/v1/system/ping \
-H "X-API-Key: MT-Robotics-AMR-Secret-Key-2026"
```

---

# 📡 API Reference

## 💻 System & Power

Base URL

```
/api/v1/system
```

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/ping` | Health Check |
| GET | `/status` | ROS2 Status (CPU, RAM, Battery, Lidar) |
| GET | `/info` | Uptime และ Hardware Serial |
| POST | `/reboot?force=false` | รีบูตระบบ |
| POST | `/poweroff?force=false` | ปิดเครื่อง |
| POST | `/license/save` | บันทึก License Key |
| GET | `/license/read` | อ่าน License Key |

---

## ⚙️ Process Management

Base URL

```
/api/v1/process
```

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/launch/{user}/{mode}` | เริ่ม Process |
| POST | `/stop/{mode}` | หยุด Process |

ตัวอย่าง Mode

- robot
- robot_map
- robot_nav

---

## 🗺️ Map Management

Base URL

```
/api/v1/map
```

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/save/{map_name}` | บันทึกแผนที่ |
| GET | `/list` | แสดงรายการแผนที่ |

ไฟล์แผนที่จะถูกบันทึกไว้ที่

```
/opt/ros2go/maps
```

---

## 🛑 Safety

Base URL

```
/api/v1/estop
```

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/trigger` | Software Emergency Stop |

เมื่อเรียกใช้งาน API นี้ ระบบจะ Publish ความเร็วเป็น

```
0.0
```

ไปยัง Topic

```
/cmd_vel
```

ทันที

---

# ⚙️ Run as Systemd Service

สำหรับการใช้งานจริง แนะนำให้รันผ่าน **Systemd**

สร้างไฟล์

```bash
sudo nano /etc/systemd/system/ros2go_api.service
```

ใส่เนื้อหาดังนี้

```ini
[Unit]
Description=ROS2Go AMR API Server
After=network.target

[Service]
User=ubuntu
Group=ubuntu

WorkingDirectory=/home/ubuntu/ros2go_amr_api

Environment="PYTHONPATH=/home/ubuntu/ros2go_amr_api"
Environment="PYTHONUNBUFFERED=1"
Environment="ROS_DOMAIN_ID=0"

ExecStart=/bin/bash -c "source /opt/ros/jazzy/setup.bash && python3 main.py"

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

รีโหลดและเปิดใช้งาน Service

```bash
sudo systemctl daemon-reload

sudo systemctl enable ros2go_api.service

sudo systemctl start ros2go_api.service
```

ตรวจสอบสถานะ

```bash
sudo systemctl status ros2go_api.service
```

---

# 📄 License

Copyright © 2026 MT Robotics

All rights reserved.
