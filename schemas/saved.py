# from uuid import UUID
# from datetime import date

# from typing import Optional
# from pydantic import EmailStr, Field, BaseModel

# class UserBase(BaseModel):
#     user_id: UUID = Field(...)
#     email: EmailStr = Field(...)

# class UserLogin(UserBase):
#     password: str = Field(
#         ...,
#         min_length=8
#     )

# class User(UserBase):
#     first_name: str = Field(
#         ...,
#         min_length=1,
#         max_length=50
#     )
#     last_name: str = Field(
#         ...,
#         min_length=1,
#         max_length=50
#     )
#     birth_date: Optional[date] = Field(default=None)



# from datetime import datetime
# from uuid import UUID

# from pydantic import Field, BaseModel

# from models.user import User

# class TweetBase(BaseModel):
#     tweet_id: UUID = Field(...)
#     content: str = Field(
#         ...,
#         max_length=256
#     )
#     created_at: datetime = Field(default=datetime.now().date())
#     by: User = Field(...)