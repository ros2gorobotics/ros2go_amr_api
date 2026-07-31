import rclpy
from rclpy.node import Node
from ros2gobot_msgs.msg import RobotStatus
from geometry_msgs.msg import Twist

import state  # ดึง state มาใช้อัปเดตสถานะ

class ApiServerNode(Node):
    def __init__(self):
        super().__init__("api_server_node")
        self.subscription = self.create_subscription(
            RobotStatus, "/robot/status", self.status_callback, 10
        )
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def status_callback(self, msg):
        # อัปเดตข้อมูลลง Global State
        state.latest_status = {
            "cpu": msg.cpu,
            "ram": msg.ram,
            "nav": msg.navigation_active,
            "map": msg.mapping_active,
            "lidar": msg.lidar_status,
            "battery": msg.battery
        }

def run_ros2():
    rclpy.init()
    state.ros2_node_instance = ApiServerNode()

    try:
        rclpy.spin(state.ros2_node_instance)
    except KeyboardInterrupt:
        pass
    finally:
        if state.ros2_node_instance:
            state.ros2_node_instance.destroy_node()
        rclpy.shutdown()