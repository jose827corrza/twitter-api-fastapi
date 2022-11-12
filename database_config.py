from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.environ['POSTGRES_USER']
db_psswrd = os.environ['POSTGRES_PASSWORD']
db_name = os.environ['POSTGRES_DB']
db_host = os.environ['HOST']
db_port = os.environ['PORT']

SQLALCHEMY_DB_URL = f"postgresql://{db_user}:{db_psswrd}@{db_host}:{db_port}/{db_name}"

def url():
    print(SQLALCHEMY_DB_URL)

engine = create_engine(SQLALCHEMY_DB_URL)

conn = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# if __name__ == '__main__':
#     url()