from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class UserSchema(Base):
    __tablename__ = 'users'

    user_uuid = Column(String, primary_key = True)
    phone_number = Column(String, nullable = False)
    password = Column(String, nullable = False)
    created_at = Column(DateTime, nullable = False, server_default = func.now())

class GoodSchema(Base):
    __tablename__ = 'goods'

    goods_id = Column(Integer, primary_key = True, autoincrement = True)
    category = Column(String(255), nullable = False)
    original_cost = Column(Integer, nullable = False)
    name = Column(String(255), nullable = False)
    first_consonant = Column(String(255), nullable = False)
    description = Column(Text, nullable = False)
    barcode_info = Column(String(255), nullable = False)
    expires_at = Column(DateTime, nullable = False)
    size =  Column(String(255), nullable = False)
    creator_id = Column(String, ForeignKey('users.user_uuid'))
    created_at = Column(DateTime, nullable = False, server_default = func.now())
    updated_at = Column(DateTime, nullable = False, server_default = func.now())
    creator = relationship('UserSchema')