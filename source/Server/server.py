import json
from typing import List
import requests
import uuid


class AgentPlataform(object):
    def __init__(self) -> None:
        # {'api_name': [nombre_endopint,args,endpoint, description]}
        pass

    def register_api(self, api_name: str, list_data: List[str]):
        # TODO falta verificar que los endopints de las apis sean validos
        with open("Data/apis.json", "r") as archivo:
            data = json.load(archivo)
        data[api_name] = list_data
        with open("Data/apis.json", "w") as archivo:
            json.dump(data, archivo)
        print(f"Api '{api_name}' registrada con exito!")
        return self.asociate_id_api(api_name)

    def get_apis(self):
        """
        Returns:
        ~~~~~~~
            _str_: Devuelve la lista de todas las APIs
        """
        with open("Data/apis.json", "r") as archivo:
            data = json.load(archivo)
        return data

    def comunicate_with_api(self, api_name, endopint_name, params=None):
        """
        Esta funcion se encarga de establecer la comunicacion con la api
        deseada, si no ocurren errores devuelve el output de la API, en otro
        caso envia un mensaje del error

        Args:
        ~~~~
            api_name (_str_): Nombre de la API
            endopint_name (_str_): Nombre del enpoint de la API a utilizar
            params (_str_, optional): _Parametros que recibe la API_. Defaults to None.

        Returns:
        ~~~~~~~
            _type_: _description_
        """
        print("Se llamo al metodo de comunicarse con la api")
        with open("Data/apis.json", "r") as archivo:
            data = json.load(archivo)
        if api_name in data.keys():
            index1 = -1
            for i, x in enumerate(data[api_name]):
                if x[1] == endopint_name:
                    index1 = i
                    break
            if index1 == -1:
                return "No se encontro el endopint"
            else:
                website = data[api_name]
                url = website[index1][3]

                # print(website)
                # print(index1)
                # print(url)
                if params != "None":
                    url = self._create_params_url(url, params)
                # print(url)
                response = requests.get(url)

                if response.status_code == 200:
                    # La solicitud fue exitosa
                    json_data = response.json()
                    # print(json_data)
                else:
                    # La solicitud no fue exitosa
                    print(
                        "La solicitud falló con el código de estado:",
                        response.status_code,
                    )
                    return "Failed"
                return str(json_data)
        else:
            return "Api doesnt match any other"

    def _create_params_url(self, website, args):
        args_ = args[1 : len(args) - 1]
        args_ = args_.split(sep=",")
        print(args_)
        print(website)
        url = website + "/".join(str(arg) for arg in args_)
        return url

    def asociate_id_api(self, api):
        id = self.generate_id()
        with open("Data/user_api_description.json", "r") as archivo:
            data = json.load(archivo)
        data[id] = [api]
        with open("Data/user_api_description.json", "w") as archivo:
            json.dump(data, archivo)
        return id

    # def update_api(self, id, api_name, endpoint, updated_api):
    #     # TODO testing
    #     # formato de cada api
    #     # nombre de la api[0], nombre del endopint, [params], direccion http, descripcion
    #     with open("Data/user_api_description.json", "r") as archivo:
    #         data = json.load(archivo)
    #     if id not in data.keys():
    #         return -1, "Invalid ID"
    #     with open("Data/apis.json", "r") as archivo:
    #         data_ = json.load(archivo)
    #     if api_name not in data_.keys():
    #         return -1, "Nombre de api invalido"
    #     index = 0
    #     for i, api in enumerate(data[api_name]):
    #         if api[1] == endpoint:
    #             index = i
    #             break
    #     data[api_name][index] = updated_api
    #     return 1, "Api udpated succefuly"

    def delete_api(self, id):
        # TODO testing
        with open("Data/user_api_description.json", "r") as archivo:
            data = json.load(archivo)
            print(data)
            print(id)
        if id not in data.keys():
            return "Error al eliminar, rectifique el id y el nombre del agente"
        else:
            with open("Data/user_api_description.json", "r") as archivo:
                data_ = json.load(archivo)
            api_name = data_[id][0]
            data_.pop(id)
            with open("Data/user_api_description.json", "w") as archivo:
                json.dump(data_, archivo)
            with open("Data/apis.json", "r") as archivo:
                data = json.load(archivo)
                data.pop(api_name)
            with open("Data/apis.json", "w") as archivo:
                json.dump(data, archivo)
            return "Agente eliminado con exito!"

    def generate_id(self):
        unique_id = uuid.uuid4()
        return str(unique_id)
