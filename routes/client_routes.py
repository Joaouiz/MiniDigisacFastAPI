from fastapi import APIRouter

from services import json_builder, gemini_service, whatsapp_service
from services.client_service import ClientService

router = APIRouter()
client_service = ClientService()

@router.get("/clients")
async def clients():
    return client_service.search_clients()

@router.get("/clients/{client_id}")
async def generate_message(client_id: int):
    clientes = client_service.search_clients()
    prompt = json_builder.defaultBuilder(clientes[client_id])

    jsonZap = json_builder.zapJson("+5541997818299", gemini_service.GerarMensagem(prompt))
    aux = whatsapp_service.enviarMensagem(jsonZap)

    print(aux)

    return "Mensagem enviada com sucesso!"