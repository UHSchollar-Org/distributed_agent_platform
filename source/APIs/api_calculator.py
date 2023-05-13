# main.py

from fastapi import FastAPI

app = FastAPI()


class Calculator_api(object):
    @app.get("/add/{x}/{y}")
    async def add(x, y):
        result = int(x) + int(y)
        return {"result": result}

    @app.get("/sub/{x}/{y}")
    async def sub(x, y):
        result = int(x) - int(y)
        return {"result": result}

    def get_url(self):
        return '/add'

    def name(self):
        return 'Calculator'

    def get_description(self):
        return '''
        Calculadora que recibe dos numros y devulve la suma estos
        '''
# example : ApiCalculator add [x,y] http://127.0.0.1:8002/add "Suma dos numeros"
