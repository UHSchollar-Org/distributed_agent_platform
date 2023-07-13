from audioop import add
from chord import Local, Daemon
from address import Address
import json
import socket
from network import *
import utils
from colorama import Fore

PORT_UDP = 9050
PORT_TCP = 9000
ip_broadcast = "192.168.1.255"


# data structure that represents a distributed hash table
class NodeAP(object):
    def __init__(self, local_address, remote_address, Bcast):
        self.daemons_ = {}
        self.my_ip = socket.gethostbyname(socket.gethostname())
        if Bcast:
            self.remote_ip = self.node_broadcast()
            print(f"Mi ip es {self.my_ip}")
            print(f"El ip del remote q respondio BC es {self.remote_ip}")
            if self.remote_ip == self.my_ip:
                remote_address = None
            else:
                remote_address = Address(self.remote_ip, PORT_TCP + 1)
            local_address = Address(self.my_ip, PORT_TCP)
            print(local_address, remote_address, "!!!!!!!!!!!!!!!!!!!")
            self.daemons_["udp_sock_listen"] = Daemon(self, "udp_sock_listen")
            self.daemons_["udp_sock_listen"].start()
        self.local_ = Local(local_address, remote_address)
        self.address = local_address
        self.shutdown_ = False
        self.daemons_["run"] = Daemon(self, "run")
        self.daemons_["run"].start()

        self.local_.start()

    def shutdown(self):
        self.local_.shutdown()
        self.shutdown_ = True

    def run(self):
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_.bind((self.my_ip, self.address.port))
        self.socket_.listen(10)
        while 1:
            try:
                conn, addr = self.socket_.accept()
                print("conexion establecida con ", addr)
            except socket.error:
                self.shutdown_ = True
                break
            request = read_from_socket(conn)
            command = request.split("|")[0]
            # we take the command out
            request = request[len(command) + 1 :]
            # defaul : "" = not respond anything
            result = json.dumps("Not response")

            result = self.dispatch(command, request, result)
            print(result, "after dispatch")
            send_to_socket(conn, result)
            conn.close()

    def dispatch(self, command, request, result):
        if command == "SET_AGENT":
            tmp = request.split(":", maxsplit=1)
            id = utils.hash(tmp[0])
            print(f"ID: {id}")
            result = self.local_.set_agent(id, key=tmp[0], value=tmp[1])
            print(result)
        if command == "GET_AGENT":
            id = utils.hash(request)
            result = self.local_.get_agent(id, request)
            print(result)
        if command == "USE_AGENT":
            tmp = request.split(" ")
            id = utils.hash(request)
            try:
                if len(tmp) == 3:
                    result = self.local_.use_agent(tmp[0], tmp[1], id, tmp[2])
                else:
                    result = self.local_.use_agent(tmp[0], tmp[1], id)
            except:
                result = "Error de solicitud"
            print(result)
        if command == "SHOW_ALL_AGENTS":
            print("EN SHOW ALL EN COMMAND DHT")
            result = self.local_.show_agents()
            print("EL RESULT DE DHT", result)
            print(result)
        if command == "DELETE":
            tmp = request.split(":")
            if len(tmp) != 2:
                result = "Error de solicitud"
            id = utils.hash(tmp[0])
            result = self.local_.delete_agent(tmp[1], id, tmp[0])
        if command == "GET_FUNC":
            result = self.local_.get_agent_functionality(request)
            print(result)

        return result

    def udp_sock_listen(self):
        print(Fore.MAGENTA, "Cree el socket UDP que escucha", Fore.RESET)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind((self.my_ip, PORT_UDP))
        while True:
            data, addr = s.recvfrom(1024)
            if addr[0] != self.my_ip:
                s.sendto(f"{self.my_ip}".encode(), addr)
                print(
                    Fore.YELLOW,
                    f"MANDE UN MENSAJE CON MI IP {self.my_ip} al {addr}",
                    Fore.RESET,
                )

    def node_broadcast(self):
        print(Fore.RED, "HACENDO BROADCAST", Fore.RESET)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(5)
        sock.sendto(b"broadcast message", (ip_broadcast, PORT_UDP))
        try:
            # Lee los datos recibidos del socket
            data, addr = sock.recvfrom(1024)
            print("received message from", addr)
            return data.decode().strip()
        except socket.timeout:
            print("no response received")
            return self.my_ip
        # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # s.settimeout(5)
        # s.sendto(b"broadcast", ("192.168.1.255", PORT_UDP))
        # try:
        #     data, addr = s.recvfrom(1024)
        #     ip_nodo = data.decode().strip()
        #     print(f"La IP del nodo es: {ip_nodo}")
        #     return ip_nodo
        # except socket.timeout:
        #     print("Tiempo de espera agotado sin respuesta")
        #     return self.my_ip


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        dht = NodeAP(
            Address(socket.gethostbyname(socket.gethostname()), PORT_TCP), None, True
        )

    elif len(sys.argv) == 4:
        dht = NodeAP(
            Address(socket.gethostbyname(socket.gethostname()), sys.argv[1]),
            Address(sys.argv[2], sys.argv[3]),
            False,
        )
    input("Press any key to shutdown\n")
    print()
    print("shuting down..")
    dht.shutdown()
    sys.exit(-1)
