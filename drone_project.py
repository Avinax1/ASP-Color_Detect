import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist, Pose

""" 
Wybrany znak: D
Pętla: Nie
Płaszczyzna: XZ
"""


class DroneController(Node):
    def __init__(self):
        super().__init__('drone_controller')

        self.gt_pose_sub = self.create_subscription(
            Pose,
            '/drone/gt_pose',
            self.pose_callback,
            1)

        self.gt_pose = None

        self.command_pub = self.create_publisher(Twist, '/drone/cmd_vel', 10)

        timer_period = 0.25
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.target = [[10.0, 0.0], [0.0, 2.5], [-2.5, 0.75], [-2.5, 0.75], [-2.5, -0.75], [-2.5, -0.75], [-2.5, -0.75], [0.0, -2.5]]
        self.next_target = 0
    
    def pose_callback(self, data):
        self.gt_pose = data

    
    def timer_callback(self):
        x = 0
        y = 0
        if self.gt_pose is not None:
            x = self.gt_pose.position.x
            y = self.gt_pose.position.y
        print(f"X: {x}, Y: {y}")

        dx = abs(x - self.target[self.next_target][0])
        dy = abs(y - self.target[self.next_target][1])

        if dx < 0.25 and dy < 0.25:
            self.target += 1
            if self.next_target > len(self.target) -1:
                self.next_target = 0

        msg = Twist()
        msg.linear.x = self.target[self.next_target][0]
        msg.linear.y = self.target[self.next_target][1]
        msg.linear.z = 20.0

        self.command_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = DroneController()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
