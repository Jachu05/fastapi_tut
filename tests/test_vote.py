from app import schemas, models
import pytest


@pytest.fixture
def test_vote(test_posts, session, test_user):


# def test_vote_on_post(authorize_client, test_posts):
#     res_vote = authorize_client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 1})
#
#     res = authorize_client.get(f"/posts/{test_posts[0].id}")
#     after_post = schemas.PostOut(**res.json())
#     assert after_post.votes == 1
#     assert res_vote.status_code == 201


def test_vote_twice(authorize_client, test_posts):
    authorize_client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 1})

    res = authorize_client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 1})

    assert res.status_code == 409
