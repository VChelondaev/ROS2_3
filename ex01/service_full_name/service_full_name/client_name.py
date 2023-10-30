import sys

from py_srvcli.srv import SummFullName
import rclpy
from rclpy.node import Node


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(SummFullName, 'summ_full_name')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = SummFullName.Request()

    def send_request(self, name, first_name, last_name):
        self.req.name = name
        self.req.first_name = first_name
        self.req.last_name = last_name
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main():
    rclpy.init()

    minimal_client = MinimalClientAsync()
    response = minimal_client.send_request(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
    minimal_client.get_logger().info(
        'Result Full Name is %s' %
        (response.full_name))

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()