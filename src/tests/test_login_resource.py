import base64
from flask import url_for
from server.routes import LoginResource


def is_login_failure(res):
    return res.status_code == 401 and res.json == {"message": "Login attempt failed"}


def do_login(client, username, password):
    bytes_ = f"{username}:{password}".encode("utf-8")
    auth = base64.b64encode(bytes_).decode("ascii")
    return client.get(url_for("login_resource"), headers={
        "Authorization": f"Basic {auth}"
    })


def test_login_no_auth(client):
    res = client.get(url_for("login_resource"))
    assert is_login_failure(res)


def test_login_no_username(client):
    res = do_login(client, None, "password")
    assert is_login_failure(res)


def test_login_no_password(client):
    res = do_login(client, "username", None)
    assert is_login_failure(res)


def test_login_unknown_user(client):
    res = do_login(client, "something", "password")
    assert is_login_failure(res)


def test_login_wrong_password(client):
    res = do_login(client, "User", "something")
    assert is_login_failure(res)


def test_login_success(client):
    res = do_login(client, "User", "snowman")
    assert res.status_code == 200
    LoginResource.token_shape.validate(res.json)
