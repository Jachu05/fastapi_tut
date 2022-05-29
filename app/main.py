import time
from typing import Optional

import psycopg2
from fastapi import FastAPI, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from sqlalchemy.orm import Session

import app.models as models
# from . import models
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_post = [
    {'title': 'asdasd', 'content': 'xdxdxdxd', 'id': 1},
    {'title': '12312312', 'content': 'e12ee1', 'id': 2},
]

port = 5433

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
async def root(db: Session = Depends(get_db)):
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    
    return {"message": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{idx}")
def get_post(idx: int):
    cursor.execute("""select * from posts where id = %s""", (idx,))
    post = cursor.fetchone()
    print(post)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {idx} was not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'post with id: {idx} was not found'}
    return {"post_det": post}


# it will make an error coz it is after get post method
# @app.get("/posts/latest")
# def get_latest_post():
#     return {'my latest post': my_post[-1]}


@app.delete("/posts/{idx}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(idx: int):
    cursor.execute("""delete from posts where id = %s returning *""", (idx,))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {idx} was not found')

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{idx}")
def update_post(post: Post, idx: int):
    cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *""",
                   (post.title, post.content, post.published, idx))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {idx} was not found')

    return {'data': updated_post}
