import requests

from services import arquive_service

def GerarMensagem(prompt):

    API_KEY = arquive_service.ler_dado("geminiKEY")
    url = arquive_service.ler_dado("geminiURL")
    headers = {
        "x-goog-api-key": f"{API_KEY}"
    }

    response = requests.post(url, headers=headers, json=prompt)

    print(response.status_code)
    print(response.text)

    textoGemini = response.json()

    return textoGemini["candidates"][0]["content"]["parts"][0]["text"]