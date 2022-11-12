# from sqlalchemy import Boolean, String, Column, DATE
# from sqlalchemy.orm import relationship

# from database_config import Base

# class User(Base):
#     __tablename__ = 'users'

#     user_id = Column(String, primary_key=True, index=True)
#     email = Column(String, unique=True)
#     password = Column(String)
#     first_name = Column(String)
#     last_name = Column(String)
#     birth_date = Column(DATE)
#     tweets = relationship('Tweet', back_populates='user_by')


# from sqlalchemy import Boolean, String, Column, Integer, DATE, ForeignKey
# from sqlalchemy.orm import relationship

# from database_config import Base
# from models.user import User

# class Tweet(Base):
#     __tablename__ = 'tweets'

#     tweet_id = Column(String, primary_key=True, index=True)
#     content = Column(String)
#     by = Column(String, ForeignKey('users.user_id'))
#     user_by = relationship('User', back_populates='tweets')

