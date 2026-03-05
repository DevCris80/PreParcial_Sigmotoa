from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from model import Pokemon, MessageBattle

lista_pokemon: list[Pokemon] = []

app = FastAPI()

@app.get("/show_all_pokemon", response_model=list[Pokemon])
def show_all_pokemon():
    return lista_pokemon

@app.get("/show_one_pokemon/{name}", response_model= Pokemon)
def show_one_pokemon(name:str):
    for pokemon in lista_pokemon:
        if pokemon.name.lower() == name.lower():
            return pokemon
    return HTTPException(status_code=404, detail=f"No se ha encontrado el pokemon {name}")

@app.get("/show_pokemon_by_ID/{id}")
def show_pokemon_by_id(id: int):
    for pokemon in lista_pokemon:
        if pokemon.id == id:
            return pokemon
    return HTTPException(status_code=404, detail=f"No existe el pokemon")

@app.get("/pokemon_battle")
def pokemon_battle(pokemon_1: str, pokemon_2: str):
    p1_obj = show_one_pokemon(pokemon_1)
    p2_obj = show_one_pokemon(pokemon_2)

    hp1 = p1_obj.life
    hp2 = p2_obj.life
    
    historial: list[MessageBattle] = []
    turno = 1

    while hp1 > 0 and hp2 > 0:
        hp2 -= p1_obj.attack
        historial.append(
            MessageBattle(
            turno=turno, 
            mensaje=f"{p1_obj.name} ataca a {p2_obj.name}. Vida de {p2_obj.name}: {max(0, hp2)}"
            )
        )
        
        if hp2 <= 0:
            historial.append(
                MessageBattle(
                    turno=turno, 
                    mensaje=f"¡{p2_obj.name} se ha debilitado! {p1_obj.name} es el ganador."
                )
            )
            break

        hp1 -= p2_obj.attack
        historial.append(
            MessageBattle(
            turno=turno, 
            mensaje=f"{p2_obj.name} contraataca a {p1_obj.name}. Vida de {p1_obj.name}: {max(0, hp1)}"
            )
        )

        if hp1 <= 0:
            historial.append(
                MessageBattle(
                    turno=turno,
                    mensaje=f"¡{p1_obj.name} se ha debilitado! {p2_obj.name} es el ganador."
                    )
                )
            break
        
        turno += 1

    return historial


@app.get("/pokemon_ordered_by")
def pokemon_ordered_by(order_by:str = "id", ascendente: bool = True):

    valid_fields = Pokemon.__fields__.keys()

    if order_by not in valid_fields:
        return HTTPException(status_code=400, detail=f"No existe el campo use: {list(valid_fields)}")

    ordenado = sorted(lista_pokemon, key=lambda x: x[order_by], reverse= not ascendente)

    return ordenado


    