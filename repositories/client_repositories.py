from models.client import Client


def coNECTAR(self, resultado):
    sapecagens = []

        for linha in resultado:
            id = linha["id"]
            nome = linha["nome"]
            telefone = linha["telefone"]
            email = linha["email"]
            valor = linha["valor"]
            vencimento = linha["vencimento"]
            status = linha["status"]

            sapecagens.append(Client(id=id, name=nome, phone=telefone, email=email, debt=valor, due_date=vencimento, status=status))

        return sapecagens