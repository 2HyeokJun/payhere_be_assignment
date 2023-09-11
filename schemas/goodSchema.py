from typing import Optional
from pydantic import BaseModel, validator, EmailStr, Field

class createGoodSchema(BaseModel):
    category: str
    original_cost: int
    name: str
    first_consonant: Optional[str] = Field(None)
    description: str
    barcode_info: str
    creator_id: Optional[str] = Field(None)
    expires_at: str
    size: str
    

    # @validator('phoneNumber', 'password')
    # def not_empty(cls, v):
    #     if not v or not v.strip():
    #         raise ValueError(f'{v} is empty.')
    #     return v

    class Config:
        from_attributes = True