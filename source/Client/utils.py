import socket


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
    ip = input("Give the ip address of a node: ")

    port = int(input("Give the port number of a node: "))

    address = Address(ip, port)

    return address.get_ip, address.get_port


def ping(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, port))
        s.sendall("\r\n".encode("utf-8"))
        s.close()
        print(f"El host {ip} en el puerto {port} está disponible.")
        return True
    except socket.error as e:
        print(f"Error al conectarse al host {ip} en el puerto {port}: {e}")
        return False
