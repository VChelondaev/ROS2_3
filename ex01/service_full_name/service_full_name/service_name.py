from py_srvcli.srv import SummFullName

import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(SummFullName, 'summ_full_name', self.summ_full_name_callback)

    def summ_full_name_callback(self, request, response):
        response.full_name = request.name + " " + request.first_name + " " + request.last_name
        self.get_logger().info('Incoming request\nname: %s \nfirst_name: %s \nlast_name: %s' % (request.name, request.first_name, request.last_name))

        return response


def main():
    rclpy.init()

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()