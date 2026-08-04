import os
import signal
import subprocess
import getpass  # เพิ่ม module getpass
from fastapi import APIRouter

import state

router = APIRouter(prefix="/process", tags=["Process"])

# ดึงชื่อ user ปัจจุบันที่รันโปรเซสนี้
current_user = getpass.getuser()

@router.post("/launch/{mode}")
async def launch( mode: str):
    if mode in state.active_processes:
        return {"status": "warning", "message": f"{mode} is already running."}

    script, command = None, None
    if mode == "robot":
        script = f"/home/{current_user}/ros2gobot/src/ros2gobot/ros2gobot_bringup/scripts/{mode}"
    elif mode in ("robot_map", "robot_nav"):
        script = f"/home/{current_user}/ros2gobot/src/ros2gobot/ros2gobot_navigation/scripts/{mode}"
    elif mode == "imu_tester":
        command = f"source /opt/ros/jazzy/setup.bash && source /home/{current_user}/bno086_ws/install/setup.bash && ros2 launch bno086_uartrvc_driver bno086_uartrvc.launch.py"
    else:
        return {"status": "error", "message": f"Unknown mode: {mode}"}

    try:
        if script:
            if not os.path.exists(script):
                return {"status": "error", "message": f"Script not found: {script}"}
            proc = subprocess.Popen([script], preexec_fn=os.setsid)
        elif command:
            proc = subprocess.Popen(["bash", "-c", command], preexec_fn=os.setsid)

        state.active_processes[mode] = proc.pid
        return {"status": "success", "message": f"Launching {mode} (PID {proc.pid})..."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/stop/{mode}")
async def stop_mode(mode: str):
    pid = state.active_processes.get(mode)
    if not pid:
        return {"status": "error", "message": f"No active process found for {mode}"}
    try:
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        state.active_processes.pop(mode, None)
        return {"status": "success", "message": f"Stopped {mode} (PID {pid})."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
