from datetime import date
from pydantic import BaseModel

class Client(BaseModel):
    id: str
    name: str
    phone: str
    email: str
    debt: float
    due_date: date
    status: str