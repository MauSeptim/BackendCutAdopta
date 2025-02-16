from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

URL_DB = os.getenv("URL")
engine = create_engine(URL_DB)
LocalSession = sessionmaker(autoflush=False, bind=engine, autocommit=False)
Base = declarative_base()

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

