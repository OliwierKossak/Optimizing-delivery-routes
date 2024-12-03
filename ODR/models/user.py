from database import Base
from sqlalchemy import String, Integer, Boolean, Column

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, index=True, primary_key=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

