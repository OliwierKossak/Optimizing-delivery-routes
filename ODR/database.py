import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

def load_cities_data(city_model, user_model):
    db = session_local()
    with open('data/cities.json') as cities:
        cities_json = json.load(cities)
        db.add_all([city_model(**city) for city in cities_json])
        db.commit()
    db.close()
