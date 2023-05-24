
from cgi import print_arguments
import threading
from Pyro5.api import Daemon, Proxy, expose, oneway
import contextlib


class Client(object):
    def __init__(self):
        self.agent_plat = Proxy('PYRONAME:AgentPlataform')
        self.abort = 0

    def give_welcome(self):
        return """
        Por favor escriba 'help' para ver las funcionalidades que se brindan.
        """

    def get_funcionality(self):
        print("""
        Para ingresar una nuevo API al servidor escriba:
        1 nombre de la api y separado por espacios
        el nombre del enpoint, [parametros separados por coma], el endpoint y la descricion, luego el signo '-' y asi sucesivamente
        ejemplo -> 1: ApiCalculator add [x,y] http://127.0.0.1:8000/add/{x}/{y} "Suma dos numeros"'

        Para escribir usar una API del servidor escriba:
        '2 Nombre de la API Nombre del endpoint [param1,param2,...]'
        ejemplo -> 2: ApiCalulator add [4,5]

        Para chequear que APIs hay en el servidor escriba:
        '3'

        Para actualizar alguna de sus APIs escriba:
        '4'
        """)

    def print_apis(self, respose):
        for api in respose.keys():
            print(f'{api} : {respose[api]}')

    @expose
    @oneway
    def message(self, nick, msg):
        if nick != self.nick:
            print('[{0}] {1}'.format(nick, msg))

    def save_user_id_api(self, api_name, list_data):
        response = self.agent_plat.asociate_id_api(
            api_name, [desc[4] for desc in list_data])
        print(response)
        if response[0] == -1:
            self.save_user_id_api(api_name, list_data)
            print('Error asociando la api con un ID')
        print(f"Id {response[0]} asociado a la api satisfactoriamente! ")

    def precess_client_input(self, line):
        temp = line.split(maxsplit=5)
        if temp[0] == 'help':
            self.get_funcionality()
        # la convencion para definir una api sera:
        # escribir 1: nombre de la api y separado por espacios
        # el nombre del enpoint, [parametros separados por coma], el endpoint y la descricion, luego el signo '-' y asi sucesivamente
        # example : ApiCalculator add [x,y] http://127.0.0.1:8000/add/{x}/{y} "Suma dos numeros"
        if temp[0] == '1':
            list_endpoints = []
            temp_ = line.split(sep='-')
            temp_[0] = temp_[0][1:]
            for i in range(0, len(temp_)):
                list_endpoints.append(temp_[i].split(maxsplit=4))
            response = self.agent_plat.register_api(
                temp[1], list_endpoints)
            print(response)
            # luego de que la api se registra con exito hay que pedir un id al cliente para asociarlo a la api
            self.save_user_id_api(temp[1], list_endpoints)
        if temp[0] == '2':
            # la convencion para comunicarse con una api sera:
            # escribir 2: nombre de la api y separado por espacio
            # el nombre del endpoint que se kiere usar
            if len(temp) == 3:
                response = self.agent_plat.comunicate_with_api(
                    temp[1], temp[2])
            elif len(temp) > 3:
                # Los parametros hay q pasarlos como una lista
                # params_list = []
                # parms = temp[3][1:len(temp[3]) - 1]
                # for x in parms.split(sep=','):
                #     params_list.append(x)
                # print(params_list)
                response = self.agent_plat.comunicate_with_api(
                    temp[1], temp[2], temp[3])
                if response[0] == -1:
                    print("Error !")
            print(response[1])
        if temp[0] == '3':
            response = self.agent_plat.get_apis()
            self.print_apis(response)

    def start(self):
        print('Ready for input! Type /quit to quit')
        print(self.give_welcome())
        try:
            with contextlib.suppress(EOFError):
                while not self.abort:
                    line = input('> ').strip()
                    if line == '/quit':
                        break
                    if line:
                        self.precess_client_input(line)

        finally:
            self.abort = 1
            self._pyroDaemon.shutdown()


class DaemonThread(threading.Thread):
    def __init__(self, user):
        threading.Thread.__init__(self)
        self.user = user
        self.daemon = True

    def run(self):
        with Daemon() as daemon:
            daemon.register(self.user)
            daemon.requestLoop(lambda: not self.user.abort)


client = Client()
daemonthread = DaemonThread(client)
daemonthread.start()
client.start()
print('Exit.')
