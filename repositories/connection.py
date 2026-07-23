import pymysql

from models.client import Client


class ClientRepository:
    def connect_database(self):
        conn = pymysql.connect(host='localhost', user="root", password="9998", database="automacao", cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")

        resultado = cursor.fetchall()
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