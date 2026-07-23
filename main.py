from fastapi import FastAPI

from repositories.connection import ClientRepository
from services.client_service import ClientService

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "API funcionando"}


@app.get("/vasco")
async def say_hello():
    connect = ClientRepository()
    return connect.connect_database()

@app.get("/clients")
async def clients():
    cs = ClientService()
    joaozinho = cs.search_clients()
    return joaozinho
