import json
from typing import List
import requests
import uuid
import os


class AgentPlataform(object):
    def __init__(self, path) -> None:
        self.apis = path + ".json"
        self.apis_id = path + "api_id" + ".json"

    def register_api(self, api_name: str, list_data: List[str]):
        with open(self.apis, "r") as archivo:
            data = json.load(archivo)
        data[api_name] = list_data
        with open(self.apis, "w") as archivo:
            json.dump(data, archivo)
        print(f"Api '{api_name}' registrada con exito!")
        return self.asociate_id_api(api_name)

    def get_apis(self):
        with open(self.apis, "r") as archivo:
            data = json.load(archivo)
        return data

    def comunicate_with_api(self, api_name, endopint_name, params_=None):
        with open(self.apis, "r") as archivo:
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
                if params_ != None:
                    params = self._create_params(params_)
                    params = dict(params)
                    try:
                        response = requests.get(url, params)
                    except requests.exceptions.ConnectionError:
                        print("Connection Error")
                else:
                    response = requests.get(url)
                if response.status_code == 200:
                    # La solicitud fue exitosa
                    json_data = response.json()
                else:
                    print(
                        "La solicitud falló con el código de estado:",
                        response.status_code,
                    )
                    return "Failed"
                return str(json_data)
        else:
            return "Api doesnt match any other"

    def _create_params(self, args):
        args_ = args[1 : len(args) - 1]
        args_ = args_.strip().split(sep=",")
        print(args_, "args_")
        params_dict = {}
        for x in args_:
            tmp = x.split(sep="=")
            params_dict[tmp[0]] = tmp[1]
        return params_dict

    def asociate_id_api(self, api):
        id = self.generate_id(api)
        with open(self.apis_id, "r") as archivo:
            data = json.load(archivo)
        data[id] = [api]
        with open(self.apis_id, "w") as archivo:
            json.dump(data, archivo)
        return id

    def delete_api_server(self, id):
        with open(self.apis_id, "r") as archivo:
            data = json.load(archivo)
        if id not in data.keys():
            return "Error al eliminar, rectifique el id y el nombre del agente"
        else:
            with open(self.apis_id, "r") as archivo:
                data_ = json.load(archivo)
            api_name = data_[id][0]
            data_.pop(id)
            with open(self.apis_id, "w") as archivo:
                json.dump(data_, archivo)
            with open(self.apis, "r") as archivo:
                data = json.load(archivo)
                data.pop(api_name)
            with open(self.apis, "w") as archivo:
                json.dump(data, archivo)
            return "Agente eliminado con exito!"

    def generate_id(self, api):
        namespace_oid = uuid.NAMESPACE_OID
        unique_id = uuid.uuid5(namespace_oid, api)
        return str(unique_id)
