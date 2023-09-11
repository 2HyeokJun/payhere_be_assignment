from typing import Optional
from pydantic import BaseModel, validator, EmailStr

class createUserSchema(BaseModel):
    phoneNumber: str
    password: str

    @validator('phoneNumber', 'password')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(f'{v} is empty.')
        return v

    class Config:
        from_attributes = True