from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from model import Pokemon, MessageBattle
from db import lista_pokemon

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
    
    historial: list[MessageBattle] = []
    turno = 1

    historial.append(MessageBattle(turno=0, mensaje=p1_obj.leavePokeball()))
    historial.append(MessageBattle(turno=0, mensaje=p2_obj.leavePokeball()))
    while p1_obj.life > 0 and p2_obj.life > 0:
        ataque_1 = p1_obj.attack(p2_obj)
        historial.append(MessageBattle(
            turno=turno,
            mensaje=ataque_1
            )
        )
        
        if p2_obj.life <= 0:
            historial.append(
                MessageBattle(
                    turno=turno, 
                    mensaje=f"¡{p2_obj.name} se ha debilitado! {p1_obj.name} es el ganador."
                )
            )
            break

        ataque_2 = p2_obj.attack(p1_obj)
        historial.append(MessageBattle(
            turno=turno,
            mensaje=ataque_2
            )
        )

        if p1_obj.life <= 0:
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


    