from ..database import Base
from sqlalchemy import Column, String, Integer

class Cities(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    start_node = Column(String, nullable=False)
    end_node = Column(String, nullable=False)
    distance = (Integer)