from sqlalchemy import String, Column, DATE, Integer, Table
from sqlalchemy.orm import relationship

from database_config import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    # birth_date = Column(DATE)
    tweets = relationship('Tweet', back_populates='owner')

# User = Table('users', Base.metadata,
#     Column("id", Integer, primary_key = True),
#     Column("user_id", String, unique = True),
#     Column("email", String, unique = True),
#     Column("hashed_password", String),
#     Column("first_name", String),
#     Column("last_name", String)
#     )