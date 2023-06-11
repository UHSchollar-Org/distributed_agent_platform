from cgi import print_arguments
from traceback import print_tb
from chord import Local, Daemon, repeat_and_sleep, inrange
from address import Address
import json
import socket
from network import *
from remote import Remote
import utils


# data structure that represents a distributed hash table
class DHT(object):
    def __init__(self, local_address, remote_address=None):
        self.local_ = Local(local_address, remote_address)
        self.address = local_address
        self.shutdown_ = False
        self.daemons_ = {}
        self.daemons_["run"] = Daemon(self, "run")
        self.daemons_["run"].start()

        self.local_.start()
        # self.local_.register_command("set", set_wrap)
        # self.local_.register_command("get", get_wrap)
        # def set_wrap(msg):
        #     return self._set(msg)

        # def get_wrap(msg):
        #     return self._get(msg)

    def shutdown(self):
        self.local_.shutdown()
        self.shutdown_ = True

    # TODO
    # el dht debe tener un socket en el q escuchar pedidos del cliente para usar get y set ya implementados aki
    def run(self):
        # should have a threadpool here :/
        # listen to incomming connections
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_.bind((self.address.ip, int(self.address.port)))
        self.socket_.listen(10)
        print("Escuchando en el puerto: ", self.address.port)
        while 1:
            try:
                conn, addr = self.socket_.accept()
                print(addr, "conexion establecida ")
            except socket.error:
                self.shutdown_ = True
                break
            request = read_from_socket(conn)
            command = request.split("|")[0]
            # we take the command out
            request = request[len(command) + 1 :]
            # defaul : "" = not respond anything
            result = json.dumps("Not response")
            if command == "SET_AGENT":
                tmp = request.split(":", maxsplit=1)
                id = utils.hash(tmp[0])
                print(f"ID: {id}")
                result = self.local_.set_agent(id, key=tmp[0], value=tmp[1].split("-"))
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
                print(tmp, " en DELETE")
                if len(tmp) != 2:
                    result = "Error de solicitud"
                id = utils.hash(tmp[0])
                result = self.local_.delete_agent(tmp[1], id, tmp[0])

                print(result, type(result))

            if command == "GET_FUNC":
                print("ENTRANDO A GET_FUNC EN DHT")
                result = self.local_.get_agent_functionality(request)
                print("RESULTADO OBTENIDO EN GET_FUNC EN DHT")
                print(result)
            
            # if command == "FINISH":
            #     print(:)
            #     conn.close()

            send_to_socket(conn, result)
            conn.close()


def create_dht(lport):
    laddress = [Address("127.0.0.1", port) for port in lport]
    r = [DHT(laddress[0])]
    for address in laddress[1:]:
        r.append(DHT(address, laddress[0]))
    return r


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        dht = DHT(Address(socket.gethostbyname(socket.gethostname()), sys.argv[1]))
    elif len(sys.argv) == 4:
        dht = DHT(Address(socket.gethostbyname(socket.gethostname()), sys.argv[1]), Address(sys.argv[2], sys.argv[3]))
    else:
        print("Invalid number of arguments received")
    input("Press any key to shutdown")
    print("shuting down..")
    dht.shutdown()
