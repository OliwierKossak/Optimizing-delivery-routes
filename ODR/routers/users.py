from database import get_db
from fastapi import APIRouter, HTTPException, status, Depends, Path
from models.user import User
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UpdateUser(BaseModel):
    email : str = None
    first_name : str = None
    last_name : str = None
    is_active : bool
    role : str = None

@router.get("/get_user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    print(user.get('role'))
    if user.get('role') is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is not None:
        return user_model
    raise HTTPException(status_code=404, detail='User not found')

@router.put("/update_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user: user_dependency, db: db_dependency, user_id: int, update_user: UpdateUser):
    if user.get('role') != 'admin' or user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    current_user = db.query(User).filter(User.id == user_id).first()
    if current_user is  None:
        raise HTTPException(status_code=404, detail='User not found')

    if current_user.email is not None:
        current_user.email = update_user.email
    if current_user.first_name is not None:
        current_user.first_name = update_user.first_name
    if current_user.last_name is not None:
        current_user.last_name = update_user.last_name
    if current_user.is_active is not None:
        current_user.is_active = update_user.is_active
    if current_user.role is not None:
        current_user.role = update_user.role

    db.add(current_user)
    db.commit()



