from fastapi import FastAPI

from routes import client_routes
from routes.client_routes import router
from routes.webhook_routes import routerHook

app = FastAPI()

app.include_router(router)
app.include_router(routerHook)

@app.get("/")
async def root():
    return {"status": "API funcionando"}

