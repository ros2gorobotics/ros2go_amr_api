# 🌐 การเข้าถึงหุ่นยนต์ผ่านชื่อ Hostname (`.local`)

แทนที่จะเชื่อมต่อกับหุ่นยนต์ผ่าน **IP Address** ซึ่งอาจเปลี่ยนแปลงทุกครั้งที่เชื่อมต่อเครือข่าย คุณสามารถเข้าถึงหุ่นยนต์ผ่าน **Hostname** ได้ เช่น

```text
http://ros2go.local:8000
```

วิธีนี้อาศัยเทคโนโลยี **mDNS (Multicast DNS)** ซึ่งช่วยให้สามารถค้นหาอุปกรณ์ภายในเครือข่าย LAN เดียวกันได้โดยไม่ต้องทราบ IP Address

บน Ubuntu และ Raspberry Pi OS จะใช้บริการ **Avahi Daemon** เพื่อประกาศชื่อ Hostname ของหุ่นยนต์บนเครือข่ายโดยอัตโนมัติ

---

# 📋 ขั้นตอนการตั้งค่า

## 1. กำหนด Hostname ของหุ่นยนต์

หากต้องการตั้งชื่อหุ่นยนต์เป็น **ros2go**

```bash
sudo hostnamectl set-hostname ros2go
```

---

## 2. แก้ไขไฟล์ `/etc/hosts`

เปิดไฟล์

```bash
sudo nano /etc/hosts
```

เพิ่มหรือแก้ไขบรรทัด

```text
127.0.1.1    ros2go
```

บันทึกไฟล์

- `Ctrl + O`
- `Enter`
- `Ctrl + X`

---

## 3. ติดตั้ง Avahi Daemon

อัปเดตแพ็กเกจ

```bash
sudo apt update
```

ติดตั้ง Avahi

```bash
sudo apt install avahi-daemon -y
```

---

## 4. เปิดใช้งาน Service

ให้ Avahi ทำงานอัตโนมัติทุกครั้งเมื่อเปิดเครื่อง

```bash
sudo systemctl enable avahi-daemon
sudo systemctl start avahi-daemon
```

ตรวจสอบสถานะ

```bash
sudo systemctl status avahi-daemon
```

หากทุกอย่างถูกต้องจะเห็นสถานะ

```text
Active: active (running)
```

---

## 5. รีบูตเครื่อง

```bash
sudo reboot
```

---

# ✅ การทดสอบ

หลังจากหุ่นยนต์เปิดขึ้นมาใหม่ และเชื่อมต่ออยู่ในเครือข่ายเดียวกับคอมพิวเตอร์

สามารถเปิดหน้า API Docs ได้ที่

```text
http://ros2go.local:8000/docs
```

หากหน้าเอกสาร FastAPI แสดงขึ้น แสดงว่าการตั้งค่าสำเร็จเรียบร้อย

---

# 💻 การใช้งานกับ React / Vite

สามารถกำหนด `baseURL` ให้เรียกผ่าน Hostname ได้เลย

```javascript
import axios from "axios";

const api = axios.create({
  baseURL: "http://ros2go.local:8000/api/v1",
  headers: {
    "X-API-Key": "MT-Robotics-AMR-Secret-Key-2026",
  },
});
```

การใช้ Hostname ทำให้ Web UI ไม่ต้องทราบ IP Address ของหุ่นยนต์ และไม่ต้องแก้ไขโค้ดเมื่อ IP เปลี่ยน

---

# 📱 อุปกรณ์ที่รองรับ

อุปกรณ์ส่วนใหญ่รองรับ **mDNS (.local)** อยู่แล้ว เช่น

- ✅ Ubuntu
- ✅ Raspberry Pi OS
- ✅ macOS
- ✅ iOS / iPadOS
- ✅ Android (ส่วนใหญ่)
- ✅ Windows 10
- ✅ Windows 11

จึงสามารถเข้าถึงหุ่นยนต์ผ่าน

```text
http://ros2go.local:8000
```

ได้ทันที โดยไม่ต้องติดตั้งซอฟต์แวร์เพิ่มเติม

---

# 💡 ข้อดีของการใช้ Hostname

- ไม่ต้องจำ IP Address ของหุ่นยนต์
- ไม่ได้รับผลกระทบเมื่อ Router แจก IP ใหม่ (DHCP)
- ตั้งค่า Web UI ได้ง่าย
- เหมาะสำหรับการติดตั้งในโรงงานหรือภายในองค์กร
- ลูกค้าเชื่อมต่อกับหุ่นยนต์ได้สะดวก เพียงใช้ชื่อ `hostname.local`

> **หมายเหตุ**
>
> การใช้งาน `hostname.local` จะทำงานได้ก็ต่อเมื่อคอมพิวเตอร์และหุ่นยนต์อยู่ใน **Local Network (LAN หรือ Wi-Fi เดียวกัน)** และบริการ **Avahi (mDNS)** ทำงานอยู่บนหุ่นยนต์
