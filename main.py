from fastapi import FastAPI
from routes.client_routes import router

app = FastAPI()

app.include_router(router)

@app.get("/")
async def root():
    return {"status": "API funcionando"}

