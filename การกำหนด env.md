# การติดตั้ง API โดยไม่ต้องแก้ไขไฟล์ Config

เพื่อให้ลูกค้าสามารถติดตั้ง **ROS2Go API** ได้ง่ายที่สุด จึงแนะนำให้ **ไม่ต้องแก้ไขไฟล์ Configuration หรือ Systemd Service ด้วยตนเอง** เช่น การเปลี่ยนชื่อผู้ใช้ (Linux User) หรือ Path ของ Workspace

แนวทางนี้ช่วยลดความผิดพลาดในการติดตั้ง และทำให้ระบบสามารถใช้งานได้แบบ **Plug-and-Play**

มีแนวทางที่แนะนำอยู่ 2 วิธี ดังนี้

---

# วิธีที่ 1: ใช้ไฟล์ Environment (`.env`) ⭐ แนะนำ

เป็นวิธีที่ยืดหยุ่นและเหมาะสำหรับการใช้งานจริง (Production)

แทนที่จะกำหนดชื่อผู้ใช้หรือ Path ไว้ภายในไฟล์ Systemd Service โดยตรง ให้แยกข้อมูลเหล่านี้ออกมาไว้ในไฟล์ `.env` แล้วให้ Systemd โหลดค่าดังกล่าวอัตโนมัติ

## 1. สร้างไฟล์ Environment

สร้างไฟล์

```text
/opt/ros2go/.env
```

ตัวอย่าง

```env
ROBOT_USER=maker
ROS_WS_PATH=/home/maker/ros2gobot
```

---

## 2. ปรับแต่งไฟล์ Systemd Service

แก้ไขไฟล์

```text
/etc/systemd/system/ros2go_api.service
```

ตัวอย่าง

```ini
[Service]
User=maker
Group=maker

WorkingDirectory=/opt/ros2go/api

# โหลดค่าจากไฟล์ .env
EnvironmentFile=/opt/ros2go/.env

Environment="PYTHONPATH=/opt/ros2go/api"
Environment="PYTHONUNBUFFERED=1"

ExecStart=/bin/bash -c "source /opt/ros/jazzy/setup.bash && source ${ROS_WS_PATH}/install/setup.bash && python3 main.py"
```

### ข้อดี

- ไม่ต้องแก้ไขไฟล์ Service ทุกครั้งที่เปลี่ยนเครื่อง
- ตัวติดตั้งสามารถสร้างไฟล์ `.env` ได้อัตโนมัติ
- ดูแลและอัปเดตระบบได้ง่าย
- รองรับการติดตั้งบนหลายเครื่องที่มีชื่อผู้ใช้แตกต่างกัน

---

# วิธีที่ 2: ใช้สคริปต์ติดตั้งอัตโนมัติ (`install.sh`)

หากต้องการให้ลูกค้าติดตั้งได้ง่ายที่สุด สามารถสร้างสคริปต์ `install.sh` เพื่อจัดการทุกขั้นตอนให้โดยอัตโนมัติ

สคริปต์จะทำหน้าที่ดังนี้

- ตรวจสอบชื่อผู้ใช้ (Linux User)
- ตรวจสอบ Home Directory
- สร้างโฟลเดอร์ที่จำเป็น
- คัดลอกไฟล์โปรแกรม
- สร้างไฟล์ Systemd Service
- เปิดใช้งาน Service อัตโนมัติ

ตัวอย่าง

```bash
#!/bin/bash

# ตรวจสอบชื่อผู้ใช้ปัจจุบัน
CURRENT_USER=$(whoami)
USER_HOME=$(eval echo ~$CURRENT_USER)

echo "Installing ROS2Go API for user: $CURRENT_USER (Home: $USER_HOME)"

# สร้างโฟลเดอร์
sudo mkdir -p /opt/ros2go/api
sudo mkdir -p /opt/ros2go/maps
sudo mkdir -p /opt/ros2go/license

# คัดลอกไฟล์โปรเจกต์
sudo cp -r . /opt/ros2go/api/
sudo chown -R $CURRENT_USER:$CURRENT_USER /opt/ros2go

# สร้างไฟล์ Systemd Service
sudo bash -c "cat > /etc/systemd/system/ros2go_api.service" <<EOF
[Unit]
Description=ROS2Go AMR API Server
After=network.target

[Service]
User=$CURRENT_USER
Group=$CURRENT_USER

WorkingDirectory=/opt/ros2go/api

Environment="PYTHONPATH=/opt/ros2go/api"
Environment="PYTHONUNBUFFERED=1"
Environment="ROS_DOMAIN_ID=0"

ExecStart=/bin/bash -c "source /opt/ros/jazzy/setup.bash && source $USER_HOME/ros2gobot/install/setup.bash && python3 main.py"

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# เปิดใช้งาน Service
sudo systemctl daemon-reload
sudo systemctl enable ros2go_api.service
sudo systemctl start ros2go_api.service

echo "Installation completed successfully!"
```

---

# วิธีการติดตั้ง

ลูกค้าเพียงรันคำสั่ง

```bash
bash install.sh
```

หลังจากนั้นสคริปต์จะดำเนินการทั้งหมดโดยอัตโนมัติ ได้แก่

- ตรวจสอบชื่อผู้ใช้ปัจจุบัน
- ตรวจสอบ Home Directory
- สร้างโฟลเดอร์ที่จำเป็น
- ติดตั้งไฟล์โปรแกรม
- สร้างไฟล์ Systemd Service ที่ถูกต้อง
- เปิดใช้งาน Service

ผู้ใช้ไม่จำเป็นต้องแก้ไขไฟล์ Configuration หรือ Systemd Service ด้วยตนเอง

---

# คำแนะนำ

| วิธี | เหมาะสำหรับ | ข้อดี |
|------|------------|--------|
| ใช้ไฟล์ `.env` | ⭐⭐⭐⭐⭐ | ยืดหยุ่น ดูแลรักษาง่าย รองรับหลายเครื่อง |
| ใช้ `install.sh` | ⭐⭐⭐⭐⭐ | ติดตั้งง่ายที่สุด ลดความผิดพลาดของผู้ใช้ |

> **แนะนำ:** สำหรับการนำไปใช้งานเชิงพาณิชย์ ควรใช้ **`install.sh` ร่วมกับไฟล์ `.env`** เพื่อให้การติดตั้งเป็นแบบอัตโนมัติ มีความยืดหยุ่น และสามารถดูแลรักษาระบบได้ง่ายในระยะยาว
