from fastapi import APIRouter
from geometry_msgs.msg import Twist

import state

router = APIRouter(prefix="/estop", tags=["Safety"])

@router.post("/trigger")
async def trigger_estop():
    if state.ros2_node_instance:
        msg = Twist()
        state.ros2_node_instance.cmd_vel_pub.publish(msg)
        return {"status": "success", "message": "Emergency Stop Triggered"}
    return {"status": "error", "message": "ROS2 API Node is not ready."}