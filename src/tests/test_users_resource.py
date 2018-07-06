import json
from flask import url_for
from server.routes import UserUtil


def test_get_all_users_unauthorized(client):
    res = client.get(url_for("users_resource"))
    assert res.status_code == 401
    assert res.json == {"msg": "Missing Authorization Header"}


def test_get_all_users_forbidden(client, user_token):
    res = client.get(url_for("users_resource"), headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert res.status_code == 403
    assert res.json == {"message": "Must be admin"}


def test_get_all_users_success(client, admin_token):
    res = client.get(url_for("users_resource"), headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert res.status_code == 200
    assert "users" in res.json
    users = res.json["users"]
    assert users
    for user in users:
        UserUtil.user_shape.validate(user)


def test_post_user_malformed(client):
    res = client.post(url_for("users_resource"),
                      content_type="application/json",
                      data=json.dumps({
                          "something": "wrong"
                      }))
    assert res.status_code == 400
    assert "message" in res.json
    assert res.json["message"] == "Input payload validation failed"


def test_post_user_already_exists(client):
    res = client.post(url_for("users_resource"),
                      content_type="application/json",
                      data=json.dumps({
                          "name": "Admin",
                          "password": "password"
                      }))
    assert res.status_code == 400
    assert "message" in res.json
    assert res.json["message"] == "A user with this name already exists"


def test_post_user_success(client):
    res = client.post(url_for("users_resource"),
                      content_type="application/json",
                      data=json.dumps({
                          "name": "New User",
                          "password": "something"
                      }))
    assert res.status_code == 200
    assert "new_user" in res.json
    UserUtil.user_shape.validate(res.json["new_user"])
