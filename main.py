#!/usr/bin/env python3

import threading
import uvicorn
from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware

# ดึงฟังก์ชันรัน ROS 2
from ros2.node import run_ros2

# ดึงระบบ Auth และ Routers ทั้งหมด
from auth import verify_api_key
from routers import system, process, safety, map

app = FastAPI(title="AMR API Server", description="ROS2GO API สำหรับควบคุมหุ่นยนต์ ROS2 SLAM Navigation")

# --- CORS Setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Router Setup ---
# *** เพิ่ม dependencies=[Depends(verify_api_key)] ตรงนี้ ***
v1_router = APIRouter(
    prefix="/api/v1",
    dependencies=[Depends(verify_api_key)]
)

# นำ Router ย่อยมาใส่ใน v1_router
v1_router.include_router(system.router)
v1_router.include_router(process.router)
v1_router.include_router(safety.router)
v1_router.include_router(map.router)

# นำ v1_router ไปใส่ใน App หลัก
app.include_router(v1_router)

def main():
    # รัน ROS2 ใน Thread แยก
    ros_thread = threading.Thread(target=run_ros2, daemon=True)
    ros_thread.start()

    # รัน FastAPI
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()
