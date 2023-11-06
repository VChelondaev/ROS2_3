import time

import numpy as np
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from tutorial_interfaces.action import MessageTurtleCommands
from geometry_msgs.msg import Twist


class CommandsActionServer(Node):

    def __init__(self):
        super().__init__('action_server')
        self._action_server = ActionServer(
            self,
            MessageTurtleCommands,
            'execute_turtle_commands',
            self.execute_callback)
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        vel = Twist()
        feedback_msg = MessageTurtleCommands.Feedback()
        if goal_handle.request.command == 'forward':
            vel.linear.x = 1.0
            for i in range(1, goal_handle.request.s+1):
                feedback_msg.odom = i
                self.get_logger().info('Feedback: %d'%feedback_msg.odom)
                self.publisher_.publish(vel)
                goal_handle.publish_feedback(feedback_msg)
                time.sleep(1)
        elif goal_handle.request.command == 'turn_right':
            vel.angular.z = -np.pi/180 * goal_handle.request.angle
            feedback_msg.odom = goal_handle.request.angle
            self.get_logger().info('Rotated at angle to right %d'%feedback_msg.odom)
            self.publisher_.publish(vel)
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1.5)
        elif goal_handle.request.command == 'turn_left':
            vel.angular.z = np.pi / 180 * goal_handle.request.angle
            feedback_msg.odom = goal_handle.request.angle
            self.get_logger().info('Rotated at angle to left %d' % feedback_msg.odom)
            self.publisher_.publish(vel)
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1.5)

        goal_handle.succeed()

        result = MessageTurtleCommands.Result()

        result.result = True
        return result


def main(args=None):
    rclpy.init(args=args)

    commands_action_server = CommandsActionServer()

    rclpy.spin(commands_action_server)


if __name__ == '__main__':
    main()