import datetime
from pydantic import BaseModel, validator, EmailStr

class getUserInfoSchema(BaseModel):
    user_id: str
    fullname: str
    email: str

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