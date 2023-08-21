import datetime
from typing import Optional
from pydantic import BaseModel, validator, EmailStr

class getUserInfoSchema(BaseModel):
    email: EmailStr
    password: Optional[str] = None

    class Config:
        orm_mode = True

class createUserSchema(BaseModel):
    fullname: str
    password: str
    email: EmailStr

    @validator('fullname', 'password', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(f'{v} is empty.')
        return v

    class Config:
        orm_mode = True

class loginUserSchema(BaseModel):
    email: EmailStr
    password: str

    @validator('email', 'password')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(f'{v} is empty.')
        return v

    class Config:
        orm_mode = True