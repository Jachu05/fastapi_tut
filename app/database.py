from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username = 'postgres'
password = 'password'
hostname = 'localhost'
database_name = 'fastapi_tut'

sqlalchemy_database_url = f'postgresql://{username}:{password}@{hostname}/{database_name}'

engine = create_engine(sqlalchemy_database_url)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
