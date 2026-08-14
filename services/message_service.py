import json
from datetime import datetime

from services import arquive_service, gemini_service, whatsapp_service, payment_service
from services.client_service import ClientService

client_service = ClientService()

def conversacao(value):

        print(json.dumps(value, indent=4, ensure_ascii=False))
        numeroMSG = value["messages"][0]["from"]
        tempoMSG = datetime.fromtimestamp(
            int(value["messages"][0]["timestamp"])
        )
        textoMSG = value["messages"][0]["text"]["body"]

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
