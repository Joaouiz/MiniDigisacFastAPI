from datetime import date

import requests

from services import arquive_service


def criarCobranca(cliente):

    token = arquive_service.ler_dado("tokenASAAS")
    url = "https://api-sandbox.asaas.com/v3/lean/payments"
    duedate = str(date.today())
    print(cliente.id)
    print(duedate)


    payload = {"billingType": "PIX",
               "customer": cliente.id,
               "value": cliente.debt,
               "dueDate": duedate}
    headers = {
        "accept": "application/json",
        "User-Agent": "Vasquinho/1.0.0",
        "content-type": "application/json",
        "access_token": token
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    print("Cobranca gerada!")


def listarCobrancas(cliente):
    token = arquive_service.ler_dado("tokenASAAS")
    url = "https://api-sandbox.asaas.com/v3/lean/payments"

    headers = {
        "accept": "application/json",
        "User-Agent": "NomeDaSuaAplicacao/1.0.0",
        "access_token": token
    }

    response = requests.get(url, headers=headers)

    print(response.text)
    idCobranca = ' '
    for cobranca in response.json()["data"]:
        if cliente.id == cobranca["customerId"]:
            idCobranca = cobranca["id"]
            print("Id cobranca encontrado!")

    return idCobranca

def gerarQRCode(id):

    token = arquive_service.ler_dado("tokenASAAS")
    url = f"https://api-sandbox.asaas.com/v3/payments/{id}/pixQrCode"

    headers = {
        "accept": "application/json",
        "User-Agent": "Vasquinho/1.0.0",
        "access_token": token
    }

    response = requests.get(url, headers=headers)

    dados = response.json()

    copiaEcola = dados["payload"]

    print(response.text)
    print("Copia e Cola feito")

    return copiaEcola