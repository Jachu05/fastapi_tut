from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import UserLogin
from ..utils import verify

router = APIRouter(tags=['Authentication'])


@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    # create token
    # return token
    return {'token': 'eg_token'}
