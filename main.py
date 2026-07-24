from fastapi import FastAPI
from routes import client_routes

app = FastAPI()

app.include_router(client_routes)

@app.get("/")
async def root():
    return {"status": "API funcionando"}

