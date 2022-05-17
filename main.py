from typing import Optional

from fastapi import FastAPI, Body
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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def root():
    return {"message": my_post}


@app.post("/posts")
def create_post(post: Post):
    print(post)
    print(post.dict())
    return {"message": post}
