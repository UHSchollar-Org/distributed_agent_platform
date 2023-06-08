#!/bin/python
from operator import le
import os
import sys
import json
import socket
import threading
import random
import time
import utils
from address import Address, inrange
from remote import Remote
from settings import *
from network import *
from utils import *
from server import AgentPlataform


def repeat_and_sleep(sleep_time):
    def decorator(func):
        def inner(self, *args, **kwargs):
            while 1:
                time.sleep(sleep_time)
                if self.shutdown_:
                    return
                ret = func(self, *args, **kwargs)
                if not ret:
                    return

        return inner

    return decorator


def retry_on_socket_error(retry_limit):
    def decorator(func):
        def inner(self, *args, **kwargs):
            retry_count = 0
            while retry_count < retry_limit:
                try:
                    ret = func(self, *args, **kwargs)
                    return ret
                except socket.error:
                    # exp retry time
                    time.sleep(2**retry_count)
                    retry_count += 1
            if retry_count == retry_limit:
                print("Retry count limit reached, aborting.. (%s)" % func.__name__)
                self.shutdown_ = True
                sys.exit(-1)

        return inner

    return decorator


# deamon to run Local's run method
class Daemon(threading.Thread):
    def __init__(self, obj, method):
        threading.Thread.__init__(self)
        self.obj_ = obj
        self.method_ = method

    def run(self):
        getattr(self.obj_, self.method_)()


class Local(object):
    def __init__(self, local_address, remote_address=None):
        new_local = Address(local_address.ip, local_address.port + 1)
        self.address_ = new_local
        print("self id = %s" % self.id())
        self.shutdown_ = False
        # list of successors
        self.successors_ = []
        # data
        self.data_ = {}
        # join the DHT
        self.join(remote_address)  # TODO problemas con el join
        # we don't have deamons until we start
        self.daemons_ = {}
        # initially no commands
        self.command_ = []
        # crear el archivo de las api y los api_id
        self.file_name = os.path.join("Data", str(utils.hash(str(self.address_))))
        # load Data
        self.load_data()
        # plataforma agente
        self.agnt_plat_server = AgentPlataform(self.file_name)

    def load_data(self):
        if os.path.exists(self.file_name + ".json"):
            with open(self.file_name + ".json", "r") as my_file:
                data_json = json.load(my_file)
                if len(data_json) != 0:
                    for x in data_json.keys():
                        self.data_[x] = data_json[x]
        else:
            file = open(self.file_name + ".json", "w")
            datos = {}
            json.dump(datos, file)
            file_id_api = open(self.file_name + "api_id" + ".json", "w")
            json.dump(datos, file_id_api)
            file.close()
            file_id_api.close()

    def __str__(self):
        return "Local %s" % self.address_

    def __repr__(self) -> str:
        return self.__str__()

    # is this id within our range?
    def is_ours(self, id):
        assert id >= 0 and id < SIZE
        return inrange(id, self.predecessor_.id(1), self.id(1))

    def shutdown(self):
        self.shutdown_ = True
        self.socket_.shutdown(socket.SHUT_RDWR)
        self.socket_.close()

    # logging function
    def log(self, info):
        """f = open("tmp//chord.log", "a+")
        f.write(str(self.id()) + " : " + info + "\n")
        f.close()
        # print str(self.id()) + " : " +  info"""

    def start(self):
        # start the daemons
        self.daemons_["run"] = Daemon(self, "run")
        self.daemons_["fix_fingers"] = Daemon(self, "fix_fingers")
        self.daemons_["stabilize"] = Daemon(self, "stabilize")
        self.daemons_["update_successors"] = Daemon(self, "update_successors")
        self.daemons_["distribute_data"] = Daemon(self, "distribute_data")
        for key in self.daemons_:
            self.daemons_[key].start()

        self.log("started")

    def ping(self):
        return True

    def join(self, remote_address=None):
        # initially just set successor
        self.finger_ = [None for x in range(LOGSIZE)]

        self.predecessor_ = None

        if remote_address:
            remote = Remote(remote_address)
            self.finger_[0] = remote.find_successor(self.id())
        else:
            self.finger_[0] = self

        self.log("joined")

    @repeat_and_sleep(STABILIZE_INT)
    @retry_on_socket_error(STABILIZE_RET)
    def stabilize(self):
        self.log("stabilize")
        suc = self.successor()
        # We may have found that x is our new successor iff
        # - x = pred(suc(n))
        # - x exists
        # - x is in range (n, suc(n))
        # - [n+1, suc(n)) is non-empty
        # fix finger_[0] if successor failed
        if suc.id() != self.finger_[0].id():
            self.finger_[0] = suc
        x = suc.predecessor()
        if (
            x != None
            and inrange(x.id(), self.id(1), suc.id())
            and self.id(1) != suc.id()
            and x.ping()
        ):
            self.finger_[0] = x
        # We notify our new successor about us
        self.successor().notify(self)
        # Keep calling us

        print("===============================================")
        print("STABILIZING")
        print("===============================================")
        print("ID: ", self.id())

        if len(self.successors_) > 0:
            print("Successors ID: ", [x.id() for x in self.successors_])

        if self.predecessor_:
            print("Predecessor ID: ", self.predecessor_.id())

        print("===============================================")
        print("=============== FINGER TABLE ==================")
        print(self.finger_)
        print("===============================================")
        print("=============== Successors ====================")
        print(self.successors_)
        print("===============================================")
        print("=============== DATA STORE ====================")
        print(str(self.data_))
        print("===============================================")
        print("+++++++++++++++ END +++++++++++++++++++++++++++")
        print()
        print()
        print()
        return True

    def notify(self, remote):
        # Someone thinks they are our predecessor, they are iff
        # - we don't have a predecessor
        # OR
        # - the new node r is in the range (pred(n), n)
        # OR
        # - our previous predecessor is dead
        self.log("notify")
        if (
            self.predecessor() == None
            or inrange(remote.id(), self.predecessor().id(1), self.id())
            or not self.predecessor().ping()
        ):
            self.predecessor_ = remote

    @repeat_and_sleep(FIX_FINGERS_INT)
    def fix_fingers(self):
        # Randomly select an entry in finger_ table and update its value
        self.log("fix_fingers")
        i = random.randrange(LOGSIZE - 1) + 1
        self.finger_[i] = self.find_successor(self.id(1 << i))
        # Keep calling us
        return True

    @repeat_and_sleep(UPDATE_SUCCESSORS_INT)
    @retry_on_socket_error(UPDATE_SUCCESSORS_RET)
    def update_successors(self):
        self.log("update successor")
        suc = self.successor()
        # if we are not alone in the ring, calculate
        if suc.id() != self.id():
            successors = [suc]
            suc_list = suc.get_successors()
            if suc_list and len(suc_list):
                successors += suc_list
            # if everything worked, we update
            self.successors_ = successors
        return True

    def get_successors(self):
        self.log("get_successors")
        return [
            (node.address_.ip, node.address_.port)
            for node in self.successors_[: N_SUCCESSORS - 1]
        ]

    def id(self, offset=0):
        id = hash(self.address_.__str__())
        return (id + offset) % SIZE

    def successor(self):
        # We make sure to return an existing successor, there `might`
        # be redundance between finger_[0] and successors_[0], but
        # it doesn't harm
        for remote in [self.finger_[0]] + self.successors_:
            if remote.ping():
                self.finger_[0] = remote
                return remote
        print("No successor available, aborting")
        self.shutdown_ = True
        sys.exit(-1)

    def predecessor(self):
        return self.predecessor_

    # @retry_on_socket_error(FIND_SUCCESSOR_RET)
    def find_successor(self, id):
        # The successor of a key can be us iff
        # - we have a pred(n)
        # - id is in (pred(n), n]
        self.log("find_successor")
        if self.predecessor() and inrange(id, self.predecessor().id(1), self.id(1)):
            return self
        node = self.find_predecessor(id)
        return node.successor()

    # @retry_on_socket_error(FIND_PREDECESSOR_RET)
    def find_predecessor(self, id):
        self.log("find_predecessor")
        node = self
        # If we are alone in the ring, we are the pred(id)
        if node.successor().id() == node.id():
            return node
        while not inrange(id, node.id(1), node.successor().id(1)):
            node = node.closest_preceding_finger(id)
        return node

    def closest_preceding_finger(self, id):
        # first fingers in decreasing distance, then successors in
        # increasing distance.
        self.log("closest_preceding_finger")
        for remote in reversed(self.successors_ + self.finger_):
            if (
                remote != None
                and inrange(remote.id(), self.id(1), id)
                and remote.ping()
            ):
                return remote
        return self

    def run(self):
        # should have a threadpool here :/
        # listen to incomming connections
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.address_)
        self.socket_.bind((self.address_.ip, int(self.address_.port)))
        self.socket_.listen(10)
        print("Escuchando en el puerto: ", self.address_.port)
        while 1:
            self.log("run loop")
            try:
                conn, addr = self.socket_.accept()
            except socket.error:
                self.shutdown_ = True
                break
            request = read_from_socket(conn)
            command = request.split(" ")[0]

            # we take the command out
            request = request[len(command) + 1 :]

            # defaul : "" = not respond anything
            result = json.dumps("")
            if command == "get_successor":
                successor = self.successor()
                result = json.dumps((successor.address_.ip, successor.address_.port))
            if command == "get_predecessor":
                # we can only reply if we have a predecessor
                if self.predecessor_ != None:
                    predecessor = self.predecessor_
                    result = json.dumps(
                        (predecessor.address_.ip, predecessor.address_.port)
                    )
            if command == "find_successor":
                successor = self.find_successor(int(request))
                result = json.dumps((successor.address_.ip, successor.address_.port))
            if command == "closest_preceding_finger":
                closest = self.closest_preceding_finger(int(request))
                result = json.dumps((closest.address_.ip, closest.address_.port))
            if command == "notify":
                npredecessor = Address(
                    request.split(" ")[0], int(request.split(" ")[1])
                )
                self.notify(Remote(npredecessor))
            if command == "get_successors":
                result = json.dumps(self.get_successors())

            if command == "set_agent":
                result = self._set(request)

            if command == "get_agent":
                api_name = request
                result = self._get(json.dumps({"key": api_name}))

            if command == "get_all_agents":
                print("COMMAND GET ALL AGENTS EN CHORD")
                result = json.dumps({"agents": list(self.data_.keys())})
                print("RESULT DEL COMMAND", result)

            if command == "use_agent":
                tmp = request.split(" ")
                result = self._use_agent(tmp[0], tmp[1], tmp[2])
                print(result)

            if command == "delete":
                api_id = request
                print(api_id, "en delete")
                result = self._delete_agent(api_id)
                print(result, "!!!")

            # or it could be a user specified operation
            for t in self.command_:
                if command == t[0]:
                    result = t[1](request)

            send_to_socket(conn, result)
            conn.close()

            if command == "shutdown":
                self.socket_.close()
                self.shutdown_ = True
                self.log("shutdown started")
                break
        self.log("execution terminated")

    def register_command(self, cmd, callback):
        self.command_.append((cmd, callback))

    def unregister_command(self, cmd):
        self.commands_ = [t for t in self.commands_ if t[0] != cmd]

    def set_agent(self, id: str, key: str, value: str):
        succ = self.find_successor(id)

        if succ.address_ != self.address_:
            result = succ.set_agent_remote(json.dumps({"key": key, "value": value}))
            return result
        else:
            return succ._set(json.dumps({"key": key, "value": value}))

    def get_agent(self, id: str, api_name: str):
        succ = self.find_successor(id)

        if succ.address_ != self.address_:
            result = succ.get_agent_remote(api_name)
            return result
        else:
            return succ._get(json.dumps({"key": api_name}))

    def use_agent(self, api_name, endpoint, id, params=None):
        succ = self.find_successor(id)
        if succ.address_ != self.address_:
            result = succ.use_agent_remote(api_name, endpoint, params)
            return result
        else:
            return succ._use_agent(api_name, endpoint, params)

    def show_agents(self):
        print("SHOW AGENTS IN CHORD")
        agents = []
        current_node = self
        print("NODO INICIAL", current_node)
        print("ID DEL NODO INICIAL", current_node.id())
        agents = agents + list(current_node.data_.keys())
        current_node = current_node.successor()
        print("SEGUNDO NODO", current_node)
        print("ID DEL SEGUNDO NODO", current_node.id())
        while current_node.address_ != self.address_:
            print("SUCCESSOR DEL NODO EN EL WHILE EN SHOW AGENTS CHORD", current_node)
            print("DENTRO DEL WHILE SHOW AGENTS")
            response = current_node.get_all_agents()
            print("RESPONSE DEL MENSAJE DEL WHILE", response)
            agents = agents + response.split()
            print("AGENTES ACTUALIZADOS", agents)

            current_node = current_node.successor()

        agents.sort()
        print("AGENTES FINALES ORDENADOS", agents)
        return json.dumps(agents)

    def delete_agent(self, id_api, id, api_name):
        succ = self.find_successor(id)
        if succ.address_ != self.address_:
            print("pal remote")
            result = succ.delete_agent_remote(id_api)
        else:
            result = succ._delete_agent(id_api, api_name)
        return result

    def _delete_agent(self, id_api: str, api_name):
        result = self.agnt_plat_server.delete_api_server(id_api)
        try:
            self.data_.pop(api_name)
        except:
            result = "Invalid api_name"
        return result

    def get_agent_functionality(self, descripcion: str):
        pass

    def _use_agent(self, api_name, endpoint, params):
        result = self.agnt_plat_server.comunicate_with_api(api_name, endpoint, params)
        return result

    def _get(self, request):
        try:
            print("EN EL _GET DE CHORD")
            print("REQUEST", request)
            data = json.loads(request)
            print("DATA", data)
            # we have the key
            return json.dumps({"status": "ok", "data": self.get(data["key"])})
        except Exception:
            # key not present
            return json.dumps({"status": "failed"})

    def _set(self, request):
        # try:
        new_ = []
        data = json.loads(request)
        for x in data["value"]:
            new_.append(x.split(" "))
        key = data["key"]
        api_id = self.set(key, new_)
        # TODO hacer q se llame a la plataforma, guardar la api, generar un id y asociar l id a la api
        return json.dumps({"status": "ok", "api_id": api_id})

        # except Exception:
        #     # something is not working
        #     return json.dumps({"status": "failed"})

    def get(self, key):
        try:
            return self.data_[key]
        except Exception:
            # not in our range
            suc = self.local_.find_successor(hash(key))
            if self.local_.id() == suc.id():
                # it's us but we don't have it
                return None
            try:
                response = suc.command("get %s" % json.dumps({"key": key}))
                if not response:
                    raise Exception
                value = json.loads(response)
                if value["status"] != "ok":
                    raise Exception
                return value["data"]
            except Exception:
                return None

    def set(self, key, value):
        # eventually it will distribute the keys
        if key in self.data_.keys():
            return "This agent already exist"
        else:
            self.data_[key] = value
            return self.agnt_plat_server.register_api(key, value)

    @repeat_and_sleep(5)
    def distribute_data(self):
        to_remove = []
        # to prevent from RTE in case data gets updated by other thread
        keys = list(self.data_.keys())
        for key in keys:
            if self.predecessor() and not inrange(
                hash(key), self.predecessor().id(1), self.id(1)
            ):
                try:
                    node = self.find_successor(hash(key))
                    node.command(
                        "set %s" % json.dumps({"key": key, "value": self.data_[key]})
                    )
                    # print "moved %s into %s" % (key, node.id())
                    to_remove.append(key)
                    print("migrated")
                except socket.error:
                    print("error migrating")
                    # we'll migrate it next time
                    pass
        # remove all the keys we do not own any more
        for key in to_remove:
            del self.data_[key]
        # Keep calling us
        return True


if __name__ == "__main__":
    import sys

    ip = "127.0.0.1"

    if len(sys.argv) == 3:
        print("JOINING RING")

        node = Local(Address(ip, sys.argv[1]), Address(ip, sys.argv[2]))
        node.start()

    if len(sys.argv) == 2:
        print("CREATING RING")
        node = Local(Address(ip, sys.argv[1]))

        node.predecessor_ = node
        node.successors_ = [node] * N_SUCCESSORS
        node.start()

    """old things 
    if len(sys.argv) == 2:
        local = Local(Address("127.0.0.1", sys.argv[1]))
    else:
        local = Local(Address("127.0.0.1", sys.argv[1]), Address(
            "127.0.0.1", sys.argv[2]))
    local.start() """
