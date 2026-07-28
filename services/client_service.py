from repositories.ClientRepository import ClientRepository

class ClientService:
    def search_clients(self):
        cr = ClientRepository()

        return cr.connect_database()