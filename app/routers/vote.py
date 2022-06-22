from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..oauth2 import get_current_user
from ..schemas import VoteData

router = APIRouter(
    prefix="/votes",
    tags=['Votes']
)


@router.get("/")
def get_votes(db: Session = Depends(get_db), current_user=Depends(get_current_user), limit: int = 10,
              skip: int = 0):
    votes = db.query(models.Vote).limit(limit).offset(skip).all()
    return votes


@router.post("/", status_code=status.HTTP_201_CREATED)
def handle_vote(vote: VoteData, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {vote.post_id} does not exist')

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on this post with id {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        message = {"message": 'successfully created vote'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"vote does not exist")
        vote_query.delete(synchronize_session=False)
        message = {"message": 'successfully deleted vote'}

    db.commit()
    return message
