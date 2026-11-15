POST_FIELDS = {"userId": int, "id": int, "title": str, "body": str}


def _assert_json(response):
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected JSON content type, got {content_type!r}"
    return response.json()


def _assert_post_shape(post):
    assert isinstance(post, dict), f"Expected a post object, got {type(post).__name__}"
    for field, field_type in POST_FIELDS.items():
        assert field in post, f"Missing field {field!r} in {post!r}"
        assert isinstance(post[field], field_type), (
            f"Field {field!r} should be {field_type.__name__}, got {post[field]!r}"
        )


def test_get_post_by_id(api_client):
    response = api_client.get("/posts/1")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    post = _assert_json(response)
    _assert_post_shape(post)
    assert post["id"] == 1, f"Expected post id 1, got {post['id']}"
    assert post["title"].strip(), "Expected a non-empty title"


def test_get_posts_filtered_by_user(api_client):
    response = api_client.get("/posts", params={"userId": 1})

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    posts = _assert_json(response)
    assert isinstance(posts, list), f"Expected a list, got {type(posts).__name__}"
    assert len(posts) == 10, f"Expected 10 posts for user 1, got {len(posts)}"
    for post in posts:
        _assert_post_shape(post)
        assert post["userId"] == 1, f"Filter leaked a post from user {post['userId']}"
