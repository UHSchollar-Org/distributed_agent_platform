# main.py

from fastapi import FastAPI

app = FastAPI()


class Calculator_api(object):
    @app.get("/add/")
    async def add(x: int, y: int):
        return {"result": x + y}

    @app.get("/sub/")
    async def sub(x: int, y: int):
        return {"result": x + y}

    def name(self):
        return "Calculator"

    def get_description(self):
        return """
        Calculadora que recibe dos numros y devulve la suma estos
        """


# example : ApiCalculator add [x,y] http://127.0.0.1:8002/add "Suma dos numeros"
