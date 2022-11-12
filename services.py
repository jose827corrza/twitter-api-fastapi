from sqlalchemy.orm import Session
from sqlalchemy.sql import Update
from pydantic import EmailStr
'''
Aca es donde vengo a hacer la logica, y eso incluye hashear la psswrd
'''
from models import user as modUser, tweet as modTweet
from schemas import user as schUser, tweet as schTweet
from database_config import conn


def get_user(db: Session, user_id: int):
    return db.query(modUser.User).filter(modUser.User.id == user_id).first()

def get_user_by_email(db: Session, email: EmailStr):
    return db.query(modUser.User).filter(modUser.User.email == email).first()

def get_user_by_id(db: Session, id: int):
    return db.query(modUser.User).filter(modUser.User.id == id).first()

def get_user_by_uuid(db: Session, id: str):
    return db.query(modUser.User).filter(modUser.User.user_id == id).first()

def get_users(db: Session, skip: int = 0, limit: int = 0):
    return db.query(modUser.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schUser.UserCreate):
    fake_hash_psswd = user.hashed_password + 'jijiIsFake'
    db_user = modUser.User(email=user.email, hashed_password=fake_hash_psswd)
    db.add(db_user)#adds the instance object to the session
    db.commit()#saves the data
    db.refresh(db_user)#If contains new data, such as the generated ID
    return db_user

def update_user(db: Session, user_id: str, user: schUser.UpdateUser):
    # conn.execute(
    #     modUser.User.update()
    #     .values(first_name = user.first_name, last_name = user.last_name)
    #     .where(modUser.User.c.user_id == user_id)
    # )
    # return conn.execute(modUser.User.select().where(modUser.User.c.user_id == user_id)).first()
    pass

def get_tweets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(modTweet.Tweet).offset(skip).limit(limit).all()
#     pass

def get_tweet_by_uuid(db: Session, id: str):
    return db.query(modTweet.Tweet).filter(modTweet.Tweet.tweet_id == id).first()

def create_tweet(db: Session, tweet: schTweet.TweetBase, user_id: str):
    # db_item = modTweet.Tweet(**tweet.dict(), owner_id = user_id)#.dict() generates a dict rep of the model, and the ** copies it, later on we add the owner
    # db.add(db_item)
    # db.commit()
    # return db.refresh(db_item)
    pass