import datetime
from pydantic import BaseModel

class getUserInfoSchema(BaseModel):
    user_id: str
    fullname: str
    email: str

class createUserSchema(BaseModel):
    fullname: str
    password: str
    email: str

    class Config:
        orm_mode = True