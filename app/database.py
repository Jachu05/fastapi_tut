from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

username = 'postgres'
password = 'password'
hostname = 'localhost'
database_name = 'fastapi_tut'

sqlalchemy_database_url = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

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

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',
#                                 database='fastapi_tut',
#                                 user='postgres',
#                                 password='password',
#                                 cursor_factory=RealDictCursor,
#                                 port=5432)
#         cursor = conn.cursor()
#         print('database connection was successful')
#         break
#     except Exception as error:
#         print("connecting to database failed", error)
#         time.sleep(2)
