import json
from datetime import datetime

import dateutil.utils
from fastapi import APIRouter, Request, Query
from starlette.responses import PlainTextResponse

from services import arquive_service, gemini_service, whatsapp_service, payment_service
from services.message_service import client_service

routerHook = APIRouter()
mensagens_processadas = set()

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
    value = dados["entry"][0]["changes"][0]["value"]

    if "messages" in value:
        mensagem = value["messages"][0]
        id_mensagem = mensagem["id"]

        if id_mensagem in mensagens_processadas:
            print("Mensagem duplicada ignorada:", id_mensagem)
            return {"status": "ok"}

        mensagens_processadas.add(id_mensagem)

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

        if "Gerar PIX" in textoMSG:
            payment_service.criarCobranca(clienteEncontrado)
            idCobranca = payment_service.listarCobrancas(clienteEncontrado)
            copiaEcola = payment_service.gerarQRCode(idCobranca)

            wow = "Seu Pix Copia e Cola eh: " + copiaEcola + "\nA data de vencimento eh hoje, podendo pagar ate o fim do dia"
            jsonZap = arquive_service.zapJson(numeroMSG, wow)
            whatsapp_service.enviarMensagem(jsonZap)
            arquive_service.gerar_contexto(idCliente, wow, str(dateutil.utils.today()), "IA")

            return {"status": "ok"}

        else:
            promptGemini = arquive_service.defaultBuilder(
                clienteEncontrado, arquive_service.ler_contexto(idCliente)
            )

            respostaGemini = gemini_service.GerarMensagem(promptGemini)
            arquive_service.gerar_contexto(idCliente, respostaGemini, str(dateutil.utils.today()), "IA")

            jsonZap = arquive_service.zapJson(
                numeroMSG, respostaGemini
            )

            whatsapp_service.enviarMensagem(jsonZap)

            return {"status": "ok"}

    elif "statuses" in value:
        print("Meta mandando status!\n")
        return {"status": "ok"}
    else:
        print("Alguma outra parada!\n")
        return {"status": "ok"}