from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, utils
from ..database import get_db
from ..schemas import UserOut, UserCreate

router = APIRouter()


@router.get("/users", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()

    users = db.query(models.User).all()

    return users


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # hash password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/users/{idx}", response_model=UserOut)
def get_user(idx: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == idx).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {idx} does not exist")

    return user
