from pydantic import BaseModel 

class Pokemon(BaseModel):
    id: int
    name: str
    attack: float
    life: float
    type: str

class MessageBattle(BaseModel):
    turno: int
    mensaje: str