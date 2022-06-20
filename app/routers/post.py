from typing import List, Optional

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..oauth2 import get_current_user
from ..schemas import PostCreate, PostResponse, PostOut

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user=Depends(get_current_user), limit: int = 10,
              skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(
        models.Post, func.count(models.Vote.post_id).label('votes')
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{idx}", response_model=PostOut)
def get_post(idx: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute("""select * from posts where id = %s""", (idx,))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == idx).first()

    post = db.query(
        models.Post, func.count(models.Vote.post_id).label('votes')
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(
        models.Post.id == idx
    ).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {idx} was not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'post with id: {idx} was not found'}
    return post


# it will make an error coz it is after get post method
# @router.get("//latest")
# def get_latest_post():
#     return {'my latest post': my_post[-1]}


@router.delete("/{idx}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(idx: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # cursor.execute("""delete from posts where id = %s returning *""", (idx,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == idx)

    deleted_post_first = deleted_post.first()

    if deleted_post_first is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {idx} was not found')

    if deleted_post_first.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorize to perform requested action')

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{idx}", response_model=PostResponse)
def update_post(updated_post: PostCreate, idx: int, db: Session = Depends(get_db),
                current_user=Depends(get_current_user)):
    # cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *""",
    #                (post.title, post.content, post.published, idx))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == idx)
    post_exec = post_query.first()

    if post_exec is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {idx} was not found')

    if post_exec.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorize to perform requested action')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_exec
