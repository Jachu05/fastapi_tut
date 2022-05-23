import time
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

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

N = 2

port = 5433

while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi_tut',
                                user='postgres',
                                password='password',
                                cursor_factory=RealDictCursor,
                                port=5433)
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


@app.get("/posts")
async def root():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"message": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    global N
    N += 1
    cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{idx}")
def get_post(idx: int):
    cursor.execute("""select * from posts where id = %s""", (idx,))
    post = cursor.fetchone()

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
    index = find_index_post(idx)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {idx} was not found')
    else:
        my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{idx}")
def update_post(post: Post, idx: int):
    index = find_index_post(idx)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {idx} was not found')

    post_dict = post.dict()
    post_dict['id'] = idx
    my_post[index] = post_dict
    return {'data': my_post}
