from pydantic import BaseModel

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