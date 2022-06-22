import pytest

from app import schemas


def test_get_all_posts(authorize_client, test_posts):
    res = authorize_client.get('/posts/')

    def _validate(post):
        return schemas.PostOut(**post)

    posts_map = map(_validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert posts_list[0].Post.id == test_posts[0].id


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_user_get_one_post_not_exist(authorize_client, test_posts):
    res = authorize_client.get("/posts/12312312312313")
    assert res.status_code == 404


def test_get_one_post(authorize_client, test_posts):
    res = authorize_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorize_client, test_user, test_posts, title, content, published):
    res = authorize_client.post("/posts/", json={"title": title, "content": content, "published": published})

    create_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert create_post.title == title


def test_create_post_default_published(authorize_client, test_posts):
    res = authorize_client.get("/posts/")

    def _validate(post):
        return schemas.PostOut(**post)

    posts_map = map(_validate, res.json())
    posts_list = list(posts_map)

    assert posts_list[0].Post.published


def test_unauthorized_create_post(client, test_posts):
    res = client.post("/posts/", json={"title": 'title', "content": 'content'})
    assert res.status_code == 401


def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorize_client, test_posts):
    res = authorize_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorize_client, test_posts):
    res = authorize_client.delete(f"/posts/3123123123123123")
    assert res.status_code == 404


def test_delete_other_user_post(authorize_client, test_posts):
    res = authorize_client.delete(f"/posts/{test_posts[4].id}")
    assert res.status_code == 403


def test_unauthorized_update_post(client, test_posts):
    data = {'title': 'updated_title',
            'content': 'updated_content'}
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401


def test_update_post_success(authorize_client, test_posts):
    data = {'title': 'updated_title',
            'content': 'updated_content'}
    res = authorize_client.put(f"/posts/{test_posts[0].id}", json=data)
    post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert post.title == data['title']
    assert post.id == test_posts[0].id


def test_update_post_non_exist(authorize_client, test_posts):
    data = {'title': 'updated_title',
            'content': 'updated_content'}
    res = authorize_client.put(f"/posts/123123123123123123123", json=data)
    assert res.status_code == 404


def test_update_other_user_post(authorize_client, test_posts):
    data = {'title': 'updated_title',
            'content': 'updated_content'}
    res = authorize_client.put(f"/posts/{test_posts[4].id}", json=data)
    assert res.status_code == 403
