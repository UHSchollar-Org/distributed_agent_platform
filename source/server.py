from Pyro5.api import Daemon, locate_ns
import Pyro5
import json
import requests
import uuid


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
        # TODO falta verificar que los endopints de las apis sean validos
        with open("Data/apis.json", "r") as archivo:
            data = json.load(archivo)
        data[api_name] = list_data
        with open("Data/apis.json", "w") as archivo:
            json.dump(data, archivo)

        print(f"Api '{api_name}' registrada con exito!")
        return {1: "Api registrada con exito!"}

    def get_apis(self):
        with open("Data/apis.json", "r") as archivo:
            data = json.load(archivo)
        return data

    def comunicate_with_api(self, api_name, endopint_name, params=None):
        #! el nombre del metodo no se esta utilzando en nada
        print('Se llamo al metodo de comunicarse con la api')
        with open("Data/apis.json", "r") as archivo:
            data = json.load(archivo)
        if api_name in data.keys():
            index1 = -1
            for i, x in enumerate(data[api_name]):
                if x[1] == endopint_name:
                    index1 = i
                    break
            if index1 == -1:
                return -1, {-1: "No se encontro el endopint"}
            else:
                website = data[api_name]
                print(website)
                print(index1)
                url = website[index1][3]
                print(url, '+++')
                if params != None:
                    url = self._create_params_url(url, params)

                    print(url)
                response = requests.get(
                    url)
                if response.status_code == 200:
                    # La solicitud fue exitosa
                    json_data = response.json()
                    print(json_data)
                else:
                    # La solicitud no fue exitosa
                    print('La solicitud falló con el código de estado:',
                          response.status_code)
                    return -1, None
                return 1, (json_data)

    def _create_params_url(self, website, args):
        args_ = args[1:len(args) - 1]
        args_ = args_.split(sep=',')
        print(args_)
        print(website)
        url = website + '/'.join(str(arg) for arg in args_)
        return url

    def asociate_id_api(self, api, description):
        id = self.generate_id()
        print('Se llamo al metodo de asociar id-api')
        print(description)
        with open("Data/user_api_description.json", "r") as archivo:
            data = json.load(archivo)
        if id in data.keys():
            return 0, {0: "El id ya existe"}
        else:
            data[id] = [api, description]
            with open("Data/user_api_description.json", "w") as archivo:
                json.dump(data, archivo)
            return id, {1: f"id: {id} asociado a la api: {api}"}

    def update_api(self, id, api_name, endpoint, updated_api):
        # TODO testing
        # formato de cada api
        # nombre de la api[0], nombre del endopint, [params], direccion http, descripcion
        with open("Data/user_api_description.json", "r") as archivo:
            data = json.load(archivo)
        if id not in data.keys():
            return -1, "Invalid ID"
        with open("Data/apis.json", "r") as archivo:
            data_ = json.load(archivo)
        if api_name not in data_.keys():
            return -1, "Nombre de api invalido"
        index = 0
        for i, api in enumerate(data[api_name]):
            if api[1] == endpoint:
                index = i
                break
        data[api_name][index] = updated_api
        return 1, "Api udpated succefuly"

    def delete_api(self, id):
        # TODO testing
        with open("Data/user_api_description.json", "r") as archivo:
            data = json.load(archivo)
        if id not in data.keys():
            return -1, "Invalid ID"
        else:
            tmp = data[id]
            api_name = tmp[0]
            data.pop(id)
            with open("Data/apis.json", "r") as archivo:
                data_ = json.load(archivo)
            data_.pop(api_name)
            return 1, "Succefuly deleted!"

    def generate_id(self):
        unique_id = uuid.uuid4()
        return str(unique_id)


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

# si se corre este metodo se eliminan todas las apis de la plataforma


def delete_json_info():
    data = {}
    with open('Data/apis.json', 'w') as archivo:
        json.dump(data, archivo)


# delete_json_info()
# a = AgentPlataform()
# print(a.get_apis())
# res = a.comunicate_with_api('Hola', 'hola')
# print(res)
