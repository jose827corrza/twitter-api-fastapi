from pydantic import BaseModel, Field

from datetime import datetime
from uuid import UUID

from pydantic import Field, BaseModel

from schemas import user

class TweetBase(BaseModel):
    # tweet_id: UUID = Field(...)
    content: str
    # created_at: datetime = Field(default=datetime.now().date())
    # by: User = Field(...)



class Tweet(TweetBase):
    id: int
    # tweet_id: str
    owner_by: int
    # owner: list[user.User] = []


    class Config:
        orm_mode = True