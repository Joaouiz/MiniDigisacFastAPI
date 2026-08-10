from datetime import date

import requests

from services import arquive_service


def criarCobranca(id, valor, dueDate):
    dueDate = date.today()

    token = arquive_service.ler_dado("./keys/tokenASAAS.txt")
    url = "https://api-sandbox.asaas.com/v3/lean/payments"

    payload = {"billingType": "PIX",
               "customerId": id,
               "value": valor,
               "dueDate": dueDate}
    headers = {
        "accept": "application/json",
        "User-Agent": "Vasquinho/1.0.0",
        "content-type": "application/json",
        "access_token": token
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

def gerarQRCode(id):

    token = arquive_service.ler_dado("./keys/tokenASAAS.txt")
    url = f"https://api-sandbox.asaas.com/v3/payments/{id}/pixQrCode"

    headers = {
        "accept": "application/json",
        "User-Agent": "Vasquinho/1.0.0",
        "access_token": token
    }

    response = requests.get(url, headers=headers)

    print(response.text)
