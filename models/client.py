from datetime import date
from pydantic import BaseModel

class Client(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    debt: float
    due_date: date
    status: str