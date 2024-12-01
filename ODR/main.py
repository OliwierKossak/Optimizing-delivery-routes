from fastapi import FastAPI
import models.cities
from database import engine
from routers import  cities
app = FastAPI()

models.cities.Base.metadata.create_engine(bind=engine)

app.include_router(cities.router)