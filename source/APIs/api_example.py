# main.py

from fastapi import FastAPI
import uvicorn

app = FastAPI()


class Hello_api(object):
    @app.get("/")
    async def hello():
        return {"message": "hello"}

    def get_url(self):
        return "192.168.1.104/"

    def get_description(self):
        return "Api que escribe hello!"

    def name(self):
        return "Hello_api"


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.1.104", port=8001)

# ApiCalculator add [x,y] http://192.168.1.104:8002/add/ "Suma dos numeros"-ApiCalculator sub [x,y] http://192.168.1.104:8002/sub/ "Resta dos numeros"
# Hola hola [] http://127.0.0.1:8001/ "Dice hola"
# uvicorn api_example:app --reload levantar server
# http://127.0.0.1:8000

# resp = requests.get("https://api.ipify.org", params) #Ipify ip [format] https://api.ipify.org "Devuelve tu ip"
# resp = requests.get("https://www.uuidtools.com/api/generate/v1") #UUID uuid [] https://www.uuidtools.com/api/generate/v1 "Devuelv un id unico"
