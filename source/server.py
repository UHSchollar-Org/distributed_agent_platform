from Pyro5.api import Daemon, locate_ns
import Pyro5
import json
import requests


@Pyro5.api.expose
@Pyro5.api.behavior(instance_mode="single")
class AgentPlataform(object):

    def __init__(self) -> None:
        # {'api_name': [nombre_endopint,args,endpoint, description]}
        self.apis = {}

    def register_api(self, api_name, list_data):
        if api_name in self.apis:
            print(f"La api '{api_name}' ya existe!")
            return 0
        #! falta verificar que los endopints de las apis sean validos
        with open("Data/datos.json", "r") as archivo:
            data = json.load(archivo)
        data[api_name] = list_data
        with open("Data/datos.json", "w") as archivo:
            json.dump(data, archivo)

        print(f"Api '{api_name}' registrada con exito!")
        return {1: "Api registrada con exito!"}

    def get_apis(self):
        with open("Data/datos.json", "r") as archivo:
            data = json.load(archivo)
        return data

    def comunicate_with_api(self, api_name, endopint_name, params=None):
        #! el nombre del metodo no se esta utilzando en nada
        print('Se llamo al metodo de comunicarse con la api')
        with open("Data/datos.json", "r") as archivo:
            data = json.load(archivo)
        if api_name in data.keys():
            index1 = -1
            for i, x in enumerate(data[api_name]):
                if x[0] == endopint_name:
                    index1 = i
                    break
            if index1 == -1:
                return {-1: "No se encontro el endopint"}
            else:
                website = data[api_name]
                response = requests.get(website[3][0])
                json_data = response.json()
                return 1, (json_data)


def main():
    with Daemon() as daemon:
        with locate_ns() as ns:
            uri_ap = daemon.register(AgentPlataform)
            # uri_ms = daemon.register(MessageServer)
            ns.register('AgentPlataform', uri_ap)
            # ns.register('MessageServer', uri_ms)
        print('AgentPlataform is Ready!')
        daemon.requestLoop()


if __name__ == '__main__':
    main()


def delete_json_info():
    data = {}
    with open('Data/datos.json', 'w') as archivo:
        json.dump(data, archivo)


# delete_json_info()
# a = AgentPlataform()
# print(a.get_apis())
# res = a.comunicate_with_api('Hola', 'hola')
# print(res)
