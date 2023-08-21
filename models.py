from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class Users(Base):
    __tablename__ = 'users'

    user_uuid = Column(String, primary_key = True)
    fullname = Column(String, nullable = False)
    password = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False)
    created_at = Column(DateTime, nullable = False, server_default = func.now())