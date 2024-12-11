from database import get_db
from fastapi import APIRouter, HTTPException, status, Depends, Path
from models.user import User
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUserRequest(BaseModel):
    email:str
    first_name: str
    last_name: str
    hashed_password: str
    is_active: bool
    role: str

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.email == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(email: str, id: int, expires_delta: timedelta):
    encode = {'sub': email, 'id': id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    print(encode)
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORYTHIM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORYTHIM])
        email: str = payload.get('sub')
        id: int = payload.get('id')
        print("payload", payload, email, id)
        if email is None or id is None:
            print("email or id none")
            raise HTTPException(status_code=401, detail='Could not validate user.')
        return {'email': email, 'id': id}
    except JWTError:
        print("JWTerror token")
        raise HTTPException(status_code=401, detail='Could not validate user.')


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.hashed_password),
        is_active=True,
        role=create_user_request.role
    )
    db.add(create_user_model)
    db.commit()

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed Authentication'
    return 'sucess'