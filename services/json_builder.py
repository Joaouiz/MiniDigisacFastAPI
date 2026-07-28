
def defaultBuilder(dadosCliente):

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