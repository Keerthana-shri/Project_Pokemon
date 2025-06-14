from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from src.schemas.pokemon_schema import PokemonInput, Ability, Stat, Type
from src.service.pokemon_service import PokemonService
from src.config.database import get_db

router = APIRouter()

def get_pokemon_service(db=Depends(get_db)):
    service = PokemonService(db)
    return service

@router.get("/pokemon/id/{pokemon_id}")
async def get_pokemon_by_id(
    pokemon_id: int,
    service: PokemonService = Depends(get_pokemon_service),
):
    pokemon = await service.fetch_pokemon_by_id(pokemon_id)
    if pokemon:
        return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")

@router.get("/pokemon/name/{pokemon_name}")
async def get_pokemon_by_name(
    pokemon_name: str,
    service: PokemonService = Depends(get_pokemon_service),
):
    pokemon = await service.fetch_pokemon_by_name(pokemon_name)
    if pokemon:
        return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")

@router.get("/pokemon")
async def get_all_pokemon(
    page: int = 1,
    limit: int = 20,
    service: PokemonService = Depends(get_pokemon_service),
):
    return await service.fetch_all_pokemon(page, limit)

@router.post("/pokemon")
async def add_pokemon(
    pokemon_data: PokemonInput,
    service: PokemonService = Depends(get_pokemon_service)
):
    try:
        pokemon_data = PokemonInput(**pokemon_data.dict())
        pokemon_id = await service.create_pokemon(pokemon_data)
        # if >20:
        #     raise HTTPException(status_code=413, detail="Cannot show more than 20 pokemons at a time")
        return {"details": "Pokemon added.", "id": pokemon_id}
    except ValidationError as e:
        raise e  # This will be caught by the custom exception handler
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/pokemon/id/{pokemon_id}")
async def update_pokemon_details(
    pokemon_id: int,
    updated_data: PokemonInput,
    service: PokemonService = Depends(get_pokemon_service),
):
    existing_pokemon = await service.fetch_pokemon_by_id(pokemon_id)
    if not existing_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    
    try:
        updated_data = PokemonInput(**updated_data.dict())
        await service.update_pokemon(pokemon_id, updated_data)
        return {"detail": "Pokemon updated successfully"}
    except ValidationError as e:
        raise e  # This will be caught by the custom exception handler
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/pokemon/id/{pokemon_id}")
async def remove_pokemon(
    pokemon_id: int,
    service: PokemonService = Depends(get_pokemon_service)
):
    pokemon = await service.fetch_pokemon_by_id(pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    
    await service.delete_pokemon(pokemon_id)
    
    return {"detail": "Pokemon deleted"}
