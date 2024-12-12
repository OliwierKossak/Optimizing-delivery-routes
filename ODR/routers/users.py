from database import get_db
from fastapi import APIRouter, HTTPException, status, Depends, Path
from models.user import User
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/get_user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    print(user.get('role'))
    if user.get('role') is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is not None:
        return user_model
    raise HTTPException(status_code=404, detail='User not found')
