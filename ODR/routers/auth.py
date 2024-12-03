from database import get_db
from fastapi import APIRouter, HTTPException, status, Depends, Path
from models.user import User
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

class CreateUserRequest(BaseModel):
    email:str
    first_name: str
    last_name: str
    hashed_password: str
    is_active: bool
    role: str

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(**create_user_request.dict())
    db.add(create_user_model)
    db.commit()

