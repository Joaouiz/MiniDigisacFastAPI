from fastapi import APIRouter

from services.client_service import ClientService

router = APIRouter()
client_service = ClientService()

@router.get("/clients")
async def clients():
    joaozinho = client_service.search_clients()
    return joaozinho