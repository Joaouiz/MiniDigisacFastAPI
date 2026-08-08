from services import arquive_service, gemini_service, whatsapp_service
from services.client_service import ClientService

client_service = ClientService()

def conversacao(contexto, nomeCliente, numeroCliente, idCliente):
    clientes = client_service.search_clients()

    prompt = arquive_service.defaultBuilder(idCliente, contexto)

    jsonZap = arquive_service.zapJson("+5541997818299", gemini_service.GerarMensagem(prompt))
    aux = whatsapp_service.enviarMensagem(jsonZap)

    print(aux)

    return 0
