from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

PG_DB = os.environ.get('POSTGRES_DB')
PG_USERNAME = os.environ.get('POSTGRES_USER')
PG_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

SQLALCHEMY_DATABASE_URL = F"postgresql://{PG_USERNAME}:{PG_PASSWORD}@localhost:5555/{PG_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
db_conn = SessionLocal()