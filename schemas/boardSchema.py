from pydantic import BaseModel

class getBoardInfoSchema(BaseModel):
    board_id: int
    board_name: str
    is_public: bool
    creator_id: str
    posts: int

    class Config:
        orm_mode = True

class createBoardSchema(BaseModel):
    board_name: str
    is_public: bool

    class Config:
        orm_mode = True

    