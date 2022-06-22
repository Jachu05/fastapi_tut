import pytest

from app import schemas, models


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorize_client, test_posts):
    res_vote = authorize_client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 1})

    res = authorize_client.get(f"/posts/{test_posts[0].id}")
    after_post = schemas.PostOut(**res.json())
    assert after_post.votes == 1
    assert res_vote.status_code == 201


def test_vote_twice(authorize_client, test_posts):
    authorize_client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 1})

    res = authorize_client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 1})

    assert res.status_code == 409


def test_vote_delete(authorize_client, test_posts, test_vote):
    res = authorize_client.post("/votes/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201


def test_delete_vote_non_exist(authorize_client, test_posts):
    res = authorize_client.post("/votes/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404


def test_vote_post_non_exist(authorize_client, test_posts):
    res = authorize_client.post("/votes/", json={"post_id": 123123123, "dir": 1})
    assert res.status_code == 404


def test_unauthorized_vote(client, test_posts):
    res = client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401
