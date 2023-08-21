import datetime
from pydantic import BaseModel

class Users(BaseModel):
    user_id: str
    fullname: str
    password: str
    email: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True