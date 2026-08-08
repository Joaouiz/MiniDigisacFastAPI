import requests

from services import arquive_service

def enviarMensagem(jsonPronto):

    token = arquive_service.ler_dado("tokenZAP")
    url = arquive_service.ler_dado("urlZAP")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=jsonPronto)

    return response.json()