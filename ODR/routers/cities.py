from database import get_db
from fastapi import APIRouter, HTTPException, status, Depends, Path
from models.cities_model import Cities
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter(
    prefix='/cities',
    tags=['city']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class CityRequest(BaseModel):
    start_node : str
    end_node : str
    distance : int = Field(gt=0)

class CityUpdate(BaseModel):
    start_node: Optional[str] = None
    end_node: Optional[str] = None
    distance: Optional[int] = Field(None, gt=0)

@router.get("/city/{city_id}", status_code=status.HTTP_200_OK)
async def get_city_by_id(db: db_dependency, city_id: int = Path(gt=0)):
    city = db.query(Cities).filter(Cities.id == city_id).first()
    if city is not None:
        return city
    raise HTTPException(status_code=404, detail='city not found')

@router.get('/get_all_cities', status_code=status.HTTP_200_OK)
async def get_all_cities(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    cities = db.query(Cities).all()
    if cities is not None:
        return cities
    raise HTTPException(status_code=404, detail='No cities in db')

@router.get('/city_routs/{city_name}', status_code=status.HTTP_200_OK)
async def get_city_routs(db: db_dependency, city_name: str):
    # add start city end city and all routs
    city_routs = db.query(Cities).filter(Cities.start_node == city_name).all()
    if city_routs is not None:
        return city_routs
    raise HTTPException(status_code=404, detail='cities routs not found')

@router.post("/add_new_city", status_code=status.HTTP_201_CREATED)
async def add_new_city(db:db_dependency, city_request: CityRequest):
    city_model = Cities(**city_request.dict())
    db.add(city_model)
    db.commit()

@router.post("/add_multiple_cities", status_code=status.HTTP_201_CREATED)
async def add_multiple_cities(db:db_dependency, cities: list[CityRequest]):
    db.add_all([Cities(**city.dict()) for city in cities])
    db.commit()

@router.put("/update_city/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_city(db: db_dependency, city: CityUpdate, city_id : int = Path(gt=0)):
    city_model = db.query(Cities).filter(Cities.id == city_id).first()
    if city_model is None:
        raise HTTPException(status_code=404, detail='city routs not found')
    if city.start_node is not None:
        city_model.start_node = city.start_node
    if city.end_node is not None:
        city_model.end_node = city.end_node
    if city.distance is not None:
        city_model.distance = city.distance

    db.commit()
    db.refresh(city_model)

@router.delete("/delete_city/{city_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city_with_all_routs(db: db_dependency, city_name: str):
    city_routs = db.query(Cities).filter((Cities.start_node == city_name) | (Cities.end_node == city_name)).all()

    if city_routs is None:
        raise HTTPException(status_code=404, detail='city routs not found')

    db.query(Cities).filter((Cities.start_node == city_name) | (Cities.end_node == city_name)).delete()
    db.commit()



