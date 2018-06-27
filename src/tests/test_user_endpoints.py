
import base64
import pytest
from flask import url_for


def get_token(client, username, password):
    bytes_ = f"{username}:{password}".encode("utf-8")
    auth = base64.b64encode(bytes_).decode("ascii")
    token_response = client.get(url_for("login_resource"), headers={
        "Authorization": f"Basic {auth}"
    })
    return token_response.json["token"]


@pytest.fixture
def admin_token(client):
    return get_token(client, "Jesus", "password")


@pytest.fixture
def user_token(client):
    return get_token(client, "Cocaine", "snowman")


def test_get_all_users_unauthorized(client):
    res = client.get(url_for("users_resource"))
    assert res.status_code == 401


#pylint: disable=W0621
def test_get_all_users_forbidden(client, user_token):
    res = client.get(url_for("users_resource"), headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert res.status_code == 403
