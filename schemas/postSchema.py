import datetime
from typing import Optional
from pydantic import BaseModel, validator, EmailStr

class getPostInfoSchema(BaseModel):
    post_id: int
    post_title: str
    post_content: str
    creator_id: str

    class Config:
        orm_mode = True

class createPostSchema(BaseModel):
    post_title: str
    post_content: str

    class Config:
        orm_mode = True