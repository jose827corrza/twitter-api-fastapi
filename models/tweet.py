from sqlalchemy import Boolean, String, Column, Integer, DATE, ForeignKey
from sqlalchemy.orm import relationship

from database_config import Base

class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, unique=True)
    content = Column(String)
    owner_by = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='tweets')