from app import schemas
# noinspection PyUnresolvedReferences
from app.models import User
from .database import client, session


def test_root(client, session):
    res = client.get("/")


def test_create_user(client, session):
    res = client.post("/users/", json={"email": "hello123@xd.pl", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@xd.pl"
    assert res.status_code == 201


def test_login_user(client, session):
    users = session.query(User).all()
    print(users)
    res = client.post("/login", data={"username": "hello123@xd.pl", "password": "password123"})

    assert res.status_code == 200
