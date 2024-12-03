from fastapi import FastAPI
from database import engine
from routers import cities, users, auth
from models import cities_model, user

app = FastAPI()

cities_model.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app.include_router(cities.router)
app.include_router(auth.router)
app.include_router(users.router)