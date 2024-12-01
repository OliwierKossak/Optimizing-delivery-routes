from ..database import Base
from sqlalchemy import String, Integer, Boolean, Column

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, index=True, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
