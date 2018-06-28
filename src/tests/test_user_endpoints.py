import pytest
from flask import url_for


def test_get_all_users_unauthorized(client):
    res = client.get(url_for("users_resource"))
    assert res.status_code == 401


def test_get_all_users_forbidden(client, user_token):
    res = client.get(url_for("users_resource"), headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert res.status_code == 403
