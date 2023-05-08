# main.py

from fastapi import FastAPI

app = FastAPI()


class Hello_api(object):
    @app.get("/")
    async def hello():
        return {"message": "hello"}

    def get_url(self):
        return "/"

    def get_description(self):
        return "Api que escribe hello!"

    def name(self):
        return "Hello_api"


class CalculatorApi(object):
    @app.get("/add/{x}/{y}")
    async def add(x, y):
        return {"result": int(x) + int(y)}

    def get_url(self):
        return '/add'

    def name(self):
        return 'Calculator'

    def get_description(self):
        return '''
        Calculadora que recibe dos numros y devulve la suma estos
        '''

# example : ApiCalculator add [x,y] http://127.0.0.1:8000/add/{x}/{y} "Suma dos numeros"
# Hola hola [] http://127.0.0.1:8000 "Dice hola"
# uvicorn api_example:app --reload levantar server
# http://127.0.0.1:8000

# with open("datos.json", "r") as archivo:
#     data = json.load(archivo)

# print(data)


# 2 Hola hola
