import requests

def GerarMensagem(prompt):

    API_KEY = ""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {
        "x-goog-api-key": f"{API_KEY}"
    }

    response = requests.post(url, headers=headers, json=prompt)

    print(response.status_code)
    print(response.text)

    textoGemini = response.json()

    return textoGemini["candidates"][0]["content"]["parts"][0]["text"]