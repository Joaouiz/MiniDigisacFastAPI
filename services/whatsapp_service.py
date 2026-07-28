import requests


def enviarMensagem(jsonPronto):

    token = ""
    url = ""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=jsonPronto)

    return response.json()