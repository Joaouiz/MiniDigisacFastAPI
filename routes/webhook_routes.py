import json


import dateutil.utils
from fastapi import APIRouter, Request, Query
from starlette.responses import PlainTextResponse

from services import arquive_service, gemini_service, whatsapp_service, payment_service, message_service
from services.message_service import client_service

routerHook = APIRouter()
#mensagens_processadas = set()

@routerHook.get("/webhook")
async def verificar_webhook(
        hub_mode: str = Query(alias="hub.mode"),
        hub_challenge: str = Query(alias="hub.challenge"),
        hub_verify_token: str = Query(alias="hub.verify_token")
):
    VERIFY_TOKEN = "VASCAO"
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge)
    else:
        return PlainTextResponse("Invalid verification token", status_code=403)

@routerHook.post("/webhook")
async def webhook(dados: dict):
    mensagens_processadas = arquive_service.lerMSGProc("msgProc")

    value = dados["entry"][0]["changes"][0]["value"]

    if "messages" in value:
        id_mensagem = value["id"]["messages"][0]

        if id_mensagem in mensagens_processadas:
            print("Mensagem duplicada ignorada:", id_mensagem)
            arquive_service.addMSGProc("msgProc", id_mensagem)
            return {"status": "ok"}

        else:
            message_service.conversacao(value)
            return {"status": "ok"}

    elif "statuses" in value:
        print("Meta mandando status!\n")
        return {"status": "ok"}
    else:
        print("Alguma outra parada!\n")
        return {"status": "ok"}