from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Users(Base):
    __tablename__ = 'users'

    user_uuid = Column(String, primary_key = True)
    fullname = Column(String, nullable = False)
    password = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False)
    created_at = Column(DateTime, nullable = False, server_default = func.now())

class Boards(Base):
    __tablename__ = 'boards'

    board_id = Column(Integer, primary_key = True, autoincrement = True)
    board_name = Column(String(255), unique = True, nullable = False)
    is_public = Column(Boolean, nullable = False)
    creator_id = Column(String, ForeignKey('users.user_uuid'))
    posts = Column(Integer, default = 0)
    creator = relationship('Users')