from sqlalchemy import  Integer, String, DateTime,Column
from datetime import datetime
from app.db.database import Base



class User(Base):
    __tablename__ = "Users"
    id  = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, index = True)
    hash_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
