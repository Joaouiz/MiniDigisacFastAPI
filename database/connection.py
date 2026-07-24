import pymysql

from models.client import Client


class ClientRepository:
    def connect_database(self):
        conn = pymysql.connect(host='localhost', user="root", password="9998", database="automacao", cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")

        resultado = cursor.fetchall()

        return resultado