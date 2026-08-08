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
            "cpu": getattr(msg, 'cpu', 0.0),
            "ram": getattr(msg, 'ram', 0.0),
            "nav": getattr(msg, 'navigation_active', False),
            "map": getattr(msg, 'mapping_active', False),
            "lidar": getattr(msg, 'lidar_status', False),
            "battery": getattr(msg, 'battery', 0.0),
            
            # 👉 เพิ่มข้อมูลเซนเซอร์ที่ขาดหายไปตรงนี้ครับ
            "imu": getattr(msg, 'imu_status', False),
            "odom": getattr(msg, 'odom_status', False),
            "tf": getattr(msg, 'tf_status', False),
            "hardware": getattr(msg, 'hardware_status', False),
            "localization": getattr(msg, 'localization_status', False)
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
