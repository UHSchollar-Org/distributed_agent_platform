# main.py

from fastapi import FastAPI

app = FastAPI()


class Calculator_api(object):
    @app.get("/add/{x}/{y}")
    async def add(x, y):
        result = int(x) + int(y)
        return {"result": result}

    def get_url(self):
        return '/add'

    def name(self):
        return 'Calculator'

    def get_description(self):
        return '''
        Calculadora que recibe dos numros y devulve la suma estos
        '''
