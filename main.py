from typing import Optional

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
    return {"message": my_post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    global N
    N += 1
    post_dict = post.dict()
    post_dict['id'] = N
    my_post.append(post_dict)
    return {"data": my_post}


@app.get("/posts/{idx}")
def get_post(idx: int):
    post = find_post(idx)
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
