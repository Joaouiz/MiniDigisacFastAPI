import json
from datetime import datetime

import dateutil.utils
from click import prompt
from fastapi import APIRouter, Request, Query
from starlette.responses import PlainTextResponse

from services import arquive_service, gemini_service, whatsapp_service
from services.message_service import client_service

routerHook = APIRouter()

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
    print(json.dumps(dados, indent=4, ensure_ascii=False))
    numeroMSG = dados["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
    tempoMSG = datetime.fromtimestamp(
        int(dados["entry"][0]["changes"][0]["value"]["messages"][0]["timestamp"])
    )
    textoMSG = dados["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]

    clientes = client_service.search_clients()
    idCliente = None
    clienteEncontrado = None

    for cliente in clientes:
        if numeroMSG == cliente.phone:
            idCliente = cliente.id
            clienteEncontrado = cliente
            break

    if idCliente is not None:
        arquive_service.gerar_contexto(idCliente, textoMSG, str(tempoMSG), "Cliente")
    else:
        print("Cliente não encontrado:", numeroMSG)
        return {"status": "ok"}

    prompt = arquive_service.defaultBuilder(
        clienteEncontrado, arquive_service.ler_contexto(idCliente)
    )

    respostaGemini = gemini_service.GerarMensagem(prompt)
    arquive_service.gerar_contexto(idCliente, respostaGemini, str(dateutil.utils.today()), "IA")

    jsonZap = arquive_service.zapJson(
        numeroMSG, respostaGemini
    )

    whatsapp_service.enviarMensagem(jsonZap)

    return {"status": "ok"}