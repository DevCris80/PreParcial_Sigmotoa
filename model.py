from pydantic import BaseModel 

class Pokemon(BaseModel):
    id: int
    name: str
    attack: float
    life: float
    type: str

    def leavePokeball(self) -> str:
        return f"{self.name}, Yo te elijo"

    def atacar(self, target_pokemon: "Pokemon") -> str:
        target_pokemon.life -= self.attack
        target_pokemon.life = max(0, target_pokemon.life) 
        
        return f"{self.name} ataca a {target_pokemon.name}. Vida restante de {target_pokemon.name}: {target_pokemon.life}"


class MessageBattle(BaseModel):
    turno: int
    mensaje: str