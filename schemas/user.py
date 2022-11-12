from pydantic import BaseModel, Field

from uuid import UUID
from datetime import date

from typing import Optional
from pydantic import EmailStr, Field, BaseModel

from schemas import tweet
class UserBase(BaseModel):
    # user_id: UUID = Field(...)
    email: EmailStr = Field(
        ...,
        description="User's email to be register",
        )

class UserCreate(UserBase):
    hashed_password: str

class User(UserBase):
    id: int
    user_id: str | None
    first_name: str | None
    last_name: str | None
    # birth_date: date
    tweets: list[tweet.Tweet] = []

    class Config:
        orm_mode = True

class UpdateUser(BaseModel):
    email: Optional[EmailStr] | None
    first_name: Optional[str] | None
    last_name: Optional[str] | None



