import os
import time
import subprocess
from fastapi import APIRouter
from pydantic import BaseModel

import config
import state

router = APIRouter(prefix="/system", tags=["System"])

# ==========================================
# Helper Functions
# ==========================================
def get_system_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            return float(f.readline().split()[0])
    except Exception:
        return -1.0

def get_pi_serial_number():
    """Read the Raspberry Pi Serial Number"""
    # Method 1: Read from Device Tree (Accurate for newer Pi models)
    try:
        with open('/sys/firmware/devicetree/base/serial-number', 'r') as f:
            # Remove Null (\x00) characters and strip whitespace
            return f.read().replace('\x00', '').strip()
    except Exception:
        pass
    
    # Method 2: Read from /proc/cpuinfo (Standard method)
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    return line.split(':')[1].strip()
    except Exception:
        pass
        
    return "UNKNOWN_SERIAL"


# ==========================================
# API Endpoints: System & Monitoring
# ==========================================
@router.get("/ping")
async def ping():
    return {"status": "ok", "message": "api v1 is running"}

@router.get("/status")
async def get_status():
    return state.latest_status

@router.get("/info")
async def system_info():
    sys_uptime = get_system_uptime()
    app_uptime = time.time() - config.SCRIPT_START_TIME
    is_just_rebooted = sys_uptime > 0 and sys_uptime < 300

    pi_serial = get_pi_serial_number()

    return {
        "status": "ready",
        "hardware_serial": pi_serial,
        "system_uptime_seconds": round(sys_uptime, 2),
        "api_uptime_seconds": round(app_uptime, 2),
        "is_just_rebooted": is_just_rebooted,
    }

@router.post("/reboot")
async def reboot_system(force: bool = False):
    is_nav_running = "robot_nav" in state.active_processes or state.latest_status.get("nav", False)
    is_map_running = "robot_map" in state.active_processes or state.latest_status.get("map", False)

    if not force and (is_map_running or is_nav_running):
        return {
            "status": "warning", 
            "message": "Robot is currently active. Please confirm again to force reboot."
        }
    try:
        subprocess.Popen(["sudo", "reboot"])
        return {"status": "success", "message": "System is rebooting..."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/poweroff")
async def poweroff_system(force: bool = False):
    is_nav_running = "robot_nav" in state.active_processes or state.latest_status.get("nav", False)
    is_map_running = "robot_map" in state.active_processes or state.latest_status.get("map", False)

    if not force and (is_map_running or is_nav_running):
        return {
            "status": "warning", 
            "message": "Robot is currently active. Please confirm again to force power off."
        }
    try:
        subprocess.Popen(["sudo", "poweroff"])
        return {"status": "success", "message": "System is shutting down..."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ==========================================
# API Endpoints: License Management
# ==========================================
class LicenseData(BaseModel):
    license_key: str

@router.post("/license/save")
async def save_license(data: LicenseData):
    """Save License Key to the OS level file"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(config.LICENSE_DIR, exist_ok=True)
        
        with open(config.LICENSE_FILE, "w") as f:
            f.write(data.license_key.strip())
        
        return {"status": "success", "message": "License saved successfully."}
        
    except PermissionError:
        return {
            "status": "error", 
            "message": f"Permission denied: API does not have write access to {config.LICENSE_DIR}. Please check directory ownership."
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to save license: {str(e)}"}

@router.get("/license/read")
async def read_license():
    """Read the current License Key from the device"""
    if not os.path.exists(config.LICENSE_FILE):
        return {
            "status": "warning", 
            "message": "No license registered on this device.", 
            "license_key": None
        }
    
    try:
        with open(config.LICENSE_FILE, "r") as f:
            key = f.read().strip()
        return {"status": "success", "license_key": key}
    except Exception as e:
        return {"status": "error", "message": f"Cannot read license file: {str(e)}"}