from flask import url_for
from server.backend import UserUtil


def test_get_user_unauthorized(client, user_public_id):
    res = client.get(url_for("user_resource", public_id=user_public_id))
    assert res.status_code == 401
    assert res.json == {"msg": "Missing Authorization Header"}


def test_get_user_forbidden(client, user_public_id, user_token):
    res = client.get(url_for("user_resource", public_id=user_public_id), headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert res.status_code == 403
    assert res.json == {"message": "Must be admin"}


def test_get_user_not_found(client, admin_token):
    res = client.get(url_for("user_resource", public_id="something"), headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert res.status_code == 404
    assert res.json == {"message": "User not found"}


def test_get_user_success(client, user_public_id, admin_token):
    res = client.get(url_for("user_resource", public_id=user_public_id), headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert res.status_code == 200
    assert "user" in res.json
    UserUtil.user_shape.validate(res.json["user"])


def test_put_user_unauthorized(client, user_public_id):
    res = client.put(url_for("user_resource", public_id=user_public_id))
    assert res.status_code == 401
    assert res.json == {"msg": "Missing Authorization Header"}


def test_put_user_forbidden(client, user_public_id, user_token):
    res = client.put(url_for("user_resource", public_id=user_public_id), headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert res.status_code == 403
    assert res.json == {"message": "Must be admin"}


def test_put_user_not_found(client, admin_token):
    res = client.put(url_for("user_resource", public_id="something"), headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert res.status_code == 404
    assert res.json == {"message": "User not found"}


def test_put_user_success(client, user_public_id, admin_token):
    res = client.put(url_for("user_resource", public_id=user_public_id), headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert res.status_code == 200
    assert "promoted_user" in res.json
    UserUtil.user_shape.validate(res.json["promoted_user"])


def test_delete_user_unauthorized(client, user_public_id):
    res = client.delete(url_for("user_resource", public_id=user_public_id))
    assert res.status_code == 401
    assert res.json == {"msg": "Missing Authorization Header"}


def test_delete_user_forbidden(client, user_public_id, user_token):
    res = client.delete(url_for("user_resource", public_id=user_public_id), headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert res.status_code == 403
    assert res.json == {"message": "Must be admin"}


def test_delete_user_not_found(client, admin_token):
    res = client.delete(url_for("user_resource", public_id="something"), headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert res.status_code == 404
    assert res.json == {"message": "User not found"}


def test_delete_user_success(client, user_public_id, admin_token):
    res = client.delete(url_for("user_resource", public_id=user_public_id), headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert res.status_code == 200
    assert "deleted_user" in res.json
    UserUtil.user_shape.validate(res.json["deleted_user"])
