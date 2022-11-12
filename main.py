from typing import Optional, List
from datetime import datetime
import os

from dotenv import load_dotenv
from pydantic import  BaseModel
from fastapi import Request
from fastapi import FastAPI, status, Path, Query, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# from schemas.user import User, UserBase, UserLogin
# from schemas.tweet import Tweet
from schemas import user as schUser, tweet as schTweet, errors as schErr
from models import user, tweet
import services

#Importante
from database_config import SessionLocal, engine
user.Base.metadata.create_all(bind=engine)
# tweet.Base.metadata.create_all(bind=engine)
# models.Base.metadata.create_all(bind=engine)

# load_dotenv()
# print(os.environ["miVar"])
# db.url()// esto era para comprobar el string de la URL DB
app = FastAPI()

###############
#DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class UnicornException(Exception):
    def __init__(self, name: str, status_code: int = 500):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=400,
        content={"statusCode": "Error creado"},
    )



@app.get('/', tags=['Home'])
def home():
    '''
    Home

    This is the principal entry point for this API, here you will find a warm greeting, watching this,
    you can be sure about:

    - The API is online
    - You are able to consume the API
    This in the main endpoint, here you will find all the tweets made until this precise moment
    '''
    return {
        "message": "Hello to Twitter API fastapi",
        "tip": "go to /docs endpoint for more info"
    }
#Tweets

@app.post(
    path='/tweet/new/{user_id}',
    status_code=status.HTTP_201_CREATED,
    tags=['Tweets'],
    summary='Post a new tweet',
    response_model= schTweet.Tweet,
    deprecated= True
    )
def new_tweet(tweet: schTweet.TweetBase,user_id: str = Path(example='3fa85f64-5717-4562-b3fc-2c963f66afa6'), db: Session = Depends(get_db)):
    db_user = services.create_tweet(db, tweet, user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return services.create_user(db=db, user=user)

@app.get(
    path='/tweets', 
    tags=['Tweets'], 
    response_model=List[schTweet.Tweet],
    status_code=status.HTTP_200_OK,
    description='List of all tweets users'
    )
def get_tweets(
    # created_date: datetime = Query(example=datetime.now().date(), default=None)
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    tweets = services.get_tweets(db, skip, limit)
    return tweets

@app.get(
    path='/tweets/{tweet_id}', 
    tags=['Tweets'], 
    # response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    description='Returns an specific tweet from the app'
    )
def get_tweets_by_user(
    tweet_id: str = Path(
        title='Unique tweet id',
        description='Unique tweet id',
        example='3fa85f64-5717-4562-b3fc-2c963f66afa6'
        ),
    db: Session = Depends(get_db)
):
    tweet = services.get_tweet_by_uuid(db, tweet_id)

# @app.delete(
#     path='/tweets/{tweet_id}',
#     status_code=status.HTTP_200_OK,
#     # response_model=Tweet,
#     tags=['Tweets'],
#     description='Deletes a tweet from the app'
#     )
# def delete_an_user():
#     pass

# @app.put(
#     path='/tweets/{tweet_id}',
#     status_code=status.HTTP_200_OK,
#     # response_model=Tweet,
#     tags=['Tweets'],
#     description='Updates an specific tweet from the app'
#     )
# def update_an_user():
#     pass
# #Users

@app.get(
    path='/users',
    response_model=List[schUser.User],
    status_code=status.HTTP_200_OK,
    tags=['Users'],
    summary='Show all the users',
    description='Returns a list of users in the app'
    )
def show_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = services.get_users(db, skip, limit)
    return users

@app.get(
    path='/users/id/{user_id}', 
    tags=['Users'], 
    response_model=schUser.User,
    status_code=status.HTTP_200_OK,
    description='Returns an specific user from the app'
    )
def show_user_by_id(
    user_id: int = Path(
        title='Unique users id',
        description='Unique users id',
        example='1'
        ),
    db: Session = Depends(get_db)
):
    user = services.get_user_by_id(db, id=user_id)
    if user == None:
        raise HTTPException(status_code=400, detail=f'The user with id:{user_id} does not exist')
    return user

@app.get(
    path='/users/{user_id}', 
    tags=['Users'], 
    response_model=schUser.User | None,
    status_code=status.HTTP_200_OK,
    description='Returns an specific user from the app, using its UUID',
    responses={
        403: {
            "model": schErr.Error, "description": "Prohibido pa"
        }
    }
    )
def show_user_by_uuid(
    user_id: str = Path(...,
        title='Unique users uuid',
        description='Unique users UUID',
        example='3fa85f64-5717-4562-b3fc-2c963f66afa6'
        ),
    db: Session = Depends(get_db)
):
    user = services.get_user_by_uuid(db, id=user_id)
    if user == None:
        raise HTTPException(status_code=400, detail=JSONResponse(schErr.Error,status_code=403))
    # f'The user with UUID:{user_id} does not exist'
    return user

# @app.delete(
#     path='/users/{user_id}',
#     status_code=status.HTTP_200_OK,
#     # response_model=User,
#     tags=['Users'],
#     description='Deletes an users from the app'
#     )
# def delete_an_user():
#     pass

@app.put(
    path='/users/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=schUser.User,
    tags=['Users'],
    description='Updates an specific user from the app',
    deprecated= True
    )
def update_an_user(
        user: schUser.UpdateUser,
        user_id: str = Path(...,
        title='Unique users uuid',
        description='Unique users UUID',
        example='3fa85f64-5717-4562-b3fc-2c963f66afa6'
        ),
    db: Session = Depends(get_db)):
    user = services.update_user(db, user_id, user)

@app.post(
    path='/signup',
    status_code=status.HTTP_201_CREATED,
    tags=['Users'],
    summary='Registers an user',
    response_model= schUser.User
    )
def signup(user: schUser.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return services.create_user(db=db, user=user)

@app.post(
    path='/login',
    response_model=schUser.User,
    status_code=status.HTTP_201_CREATED,
    tags=['Users'],
    summary='Login an user using already created credentials',
    deprecated= True
    )
def login(user: schUser.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return services.create_user(db=db, user=user)


# #test
@app.post("/users_test/", response_model=schUser.User, deprecated= True)
def create_user(user: schUser.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return services.create_user(db=db, user=user)

# response_model=list[schUser.User]
@app.get("/users_test/", response_model=List[schUser.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = services.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users_test/{user_id}", response_model=schUser.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = services.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# @app.post("/users_test/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return services.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items_test/", response_model=list[item.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = services.get_items(db, skip=skip, limit=limit)
#     return items

