from datetime import date


def defaultBuilder(dadosCliente, contexto):

    texto = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Voce ira escrever um texto breve como se fosse um atendente de IA chamado Cleitin "
                                f"que trabalha em um escritorio de advocacia focado "
                                f"em cobranca, chamado Juninho & Associados. Seu trabalho eh comunicar "
                                f"{dadosCliente.name} que ele/ela esta devendo "
                                f"{dadosCliente.debt}. Eh que a conta vence em {dadosCliente.due_date}."
                                f"Seja cordial!"
                                f"Logo em seguida vem o historico da conversa: {contexto}"
                                f"Se nao tiver historico com data da mensagem e o conteudo dela considere como se fosse o primeiro contato com o cliente. E se no contexto tiver que o cliente escreveu 'Gerar PIX' considere como enviado."
                    }
                ]
            }
        ]
    }

    return texto

def zapJson(telefone, texto):

    json = {
        "messaging_product": "whatsapp",
        "to": telefone,
        "type": "text",
        "text": {
            "body": texto
        }
    }

    return json

def gerar_contexto(id, texto, data, quemMandou):
    if quemMandou == "IA":
        with open(f"./logs/{id}.log", "a") as arquivo:
            arquivo.write("\nMensagem da IA -> " + data + ": ")
            arquivo.write(texto + "\n")
    if quemMandou == "Cliente":
        with open(f"./logs/{id}.log", "a") as arquivo:
            arquivo.write("\nMensagem cliente -> " + data + ": ")
            arquivo.write(texto + "\n")

def ler_contexto(id):
    with open(f"./logs/{id}.log", "r") as arquivo:
        contexto = arquivo.read()
    return contexto

def ler_dado(caminho):
    with open(f"./keys/{caminho}.txt", "r") as arquivo:
        dado = arquivo.read()
    return dado

def lerMSGProc(caminho):
    with open(f"./util/{caminho}.txt", "r") as arquivo:
        dado = arquivo.readlines()
    return dado

def addMSGProc(caminho, idMSG):
    with open(f"./util/{caminho}.txt", "a") as arquivo:
        arquivo.write(idMSG)