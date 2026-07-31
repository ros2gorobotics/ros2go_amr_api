import os
import glob
import subprocess
from fastapi import APIRouter

import config

router = APIRouter(prefix="/map", tags=["Map"])

@router.post("/save/{map_name}")
async def save_map(map_name: str):
    map_path = os.path.join(config.MAP_DIRECTORY, map_name)
    command = f"source /opt/ros/jazzy/setup.bash && ros2 run nav2_map_server map_saver_cli -f {map_path}"
    try:
        subprocess.run(["bash", "-c", command], check=True)
        return {"status": "success", "message": f"Map saved successfully at {map_path}"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}

@router.get("/list")
async def list_maps():
    if not os.path.exists(config.MAP_DIRECTORY):
        return {"status": "success", "maps": []}
    
    yaml_files = glob.glob(os.path.join(config.MAP_DIRECTORY, "*.yaml"))
    map_names = [os.path.basename(f).replace('.yaml', '') for f in yaml_files]
    return {"status": "success", "maps": map_names}