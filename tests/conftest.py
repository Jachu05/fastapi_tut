import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.config import settings
from app.database import Base, get_db
from app.main import app
from app.oauth2 import create_access_token

sqlalchemy_database_url = f'postgresql://{settings.database_username}:{settings.database_password}@' \
                          f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(sqlalchemy_database_url)

test_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = test_session_local()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client, session):
    user_data = {
        "email": "hello123@xd.pl",
        "password": "password123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client, session):
    user_data = {
        "email": "hello1234@xd.pl",
        "password": "password123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})


@pytest.fixture
def authorize_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        },
        {
            "title": "4rd title",
            "content": "4rd content",
            "owner_id": test_user['id']
        },
        {
            "title": "5rd title",
            "content": "5rd content",
            "owner_id": test_user2['id']
        }
    ]

    def _create_post_model(post):
        return models.Post(**post)

    post_map = map(_create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                  models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']),
    #                  models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])

    posts = session.query(models.Post).all()
    return posts
