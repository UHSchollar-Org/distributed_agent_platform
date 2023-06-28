from chord import Local, Daemon
from address import Address
import json
import socket
from network import *
import utils


# data structure that represents a distributed hash table
class NodeAP(object):
    def __init__(self, local_address, remote_address=None):
        self.local_ = Local(local_address, remote_address)
        self.address = local_address
        self.shutdown_ = False
        self.daemons_ = {}
        self.daemons_["run"] = Daemon(self, "run")
        self.daemons_["run"].start()

        self.local_.start()

    def shutdown(self):
        self.local_.shutdown()
        self.shutdown_ = True

    def run(self):
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_.bind((self.address.ip, int(self.address.port)))
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


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        dht = NodeAP(Address(socket.gethostbyname(socket.gethostname()), sys.argv[1]))
    elif len(sys.argv) == 4:
        dht = NodeAP(
            Address(socket.gethostbyname(socket.gethostname()), sys.argv[1]),
            Address(sys.argv[2], sys.argv[3]),
        )
    else:
        print("Invalid number of arguments received")
    input("Press any key to shutdown\n")
    print()
    print("shuting down..")
    dht.shutdown()
    sys.exit(-1)
