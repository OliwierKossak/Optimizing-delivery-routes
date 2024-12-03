from database import get_db
from fastapi import APIRouter, HTTPException, status, Depends, Path
from models.user import User
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['users']
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/get_user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(db: db_dependency, user_id: int = Path(gt=0)):
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is not None:
        return user_model
    raise HTTPException(status_code=404, detail='User not found')
