import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from tutorial_interfaces.action import MessageTurtleCommands
from geometry_msgs.msg import Twist


class CommandsActionClient(Node):

    def __init__(self):
        super().__init__('action_client')
        self._action_client = ActionClient(self, MessageTurtleCommands, 'execute_turtle_commands')

    def send_goal(self, comm, val):
        goal_msg = MessageTurtleCommands.Goal()
        goal_msg.command = comm
        if comm == 'forward':
            goal_msg.s = val
        elif comm == 'turn_right' or comm == 'turn_left':
            goal_msg.angle = val
        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(goal_msg)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: ' + str(result.result))
        # rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)

    action_client = CommandsActionClient()


    action_client.send_goal('forward', 2)
    action_client.send_goal('turn_right', 90)
    action_client.send_goal('forward', 1)
    try:
        rclpy.spin(action_client)
    except KeyboardInterrupt:
        print('Interrupted')
        rclpy.shutdown()


if __name__ == '__main__':
    main()