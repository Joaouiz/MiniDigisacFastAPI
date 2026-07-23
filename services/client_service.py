from datetime import date
from models.client import Client

class ClientService:
    def search_clients(self):
        joaozinho = Client(
            id=1,
            name="Joao",
            phone="40028922",
            debt=999999999999,
            due_date=date(2026,10,1),
            status="Pago"
        )

        return joaozinho