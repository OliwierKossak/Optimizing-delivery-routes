from database import get_db
from fastapi import APIRouter, HTTPException, status, Depends, Path
from models.cities_model import Cities
from pydantic import BaseModel, Field
from typing import Annotated
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/cities',
    tags=['auth']
)

db_dependency = Annotated[Session, Depends(get_db)]

class CityRequest(BaseModel):
    start_node : str
    end_node : str
    distance : int = Field(gt=0)

@router.get("/{city_id}", status_code=status.HTTP_200_OK)
async def get_city_by_id(db: db_dependency, city_id: int = Path(gt=0)):
    city = db.query(Cities).filter(Cities.id == city_id).first()
    if city is not None:
        return city
    raise HTTPException(status_code=404, detail='city not found')

@router.post("/add_new_city", status_code=status.HTTP_201_CREATED)
async def add_new_city(db:db_dependency, city_request: CityRequest):
    city_model = Cities(**city_request.dict())
    db.add(city_model)
    db.commit()
