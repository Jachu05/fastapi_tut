import time

import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

# import app.models as models
from . import models
from .database import engine
from .routers import user, post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

my_post = [
    {'title': 'asdasd', 'content': 'xdxdxdxd', 'id': 1},
    {'title': '12312312', 'content': 'e12ee1', 'id': 2},
]

port = 5432

while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi_tut',
                                user='postgres',
                                password='password',
                                cursor_factory=RealDictCursor,
                                port=5432)
        cursor = conn.cursor()
        print('database connection was successful')
        break
    except Exception as error:
        print("connecting to database failed", error)
        time.sleep(2)


def find_post(idx):
    for p in my_post:
        if p["id"] == idx:
            return p


def find_index_post(idx):
    for i, p in enumerate(my_post):
        if p["id"] == idx:
            return i


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
