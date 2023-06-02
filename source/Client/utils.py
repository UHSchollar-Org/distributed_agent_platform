import json


class Address:
    def __init__(self, ip: str, port: str):
        self.ip = ip
        self.port = port

    @property
    def get_ip(self):
        return self.ip

    @property
    def get_port(self):
        return int(self.port)


def get_ip_port():
    # ip = input("Give the ip address of a node")
    ip = "127.0.0.1"
    # port = 9000
    port = int(input("Give the port number of a node: "))

    address = Address(ip, port)

    return address.get_ip, address.get_port
