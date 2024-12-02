from fastapi import FastAPI
from database import engine
from routers import cities
from models import cities_model

app = FastAPI()

cities_model.Base.metadata.create_all(bind=engine)

app.include_router(cities.router)