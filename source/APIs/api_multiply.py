from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/multiply")
async def multiply_numbers(a: int, b: int):
    response = requests.get(f"http://localhost:8000/add?a={a}&b={b}")
    result = response.json()["result"]
    return {"result": a * result}
