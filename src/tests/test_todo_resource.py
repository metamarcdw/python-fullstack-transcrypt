from flask import url_for
from server.util import TodoUtil


def test_get_todo_unauthorized(client):
    res = client.get(url_for("todo_resource", id=2))
    assert res.status_code == 401
    assert res.json == {"msg": "Missing Authorization Header"}


def test_get_todo_not_found(client, user_token):
    res = client.get(url_for("todo_resource", id=22), headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert res.status_code == 404
    assert res.json == {
        "message": "Todo not found. You have requested this URI " +
                   "[/todo/22] but did you mean /todo/<int:id> or /todo ?"
    }


def test_get_todo_success(client, user_token):
    res = client.get(url_for("todo_resource", id=2), headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert res.status_code == 200
    assert "todo" in res.json
    TodoUtil.todo_shape.validate(res.json["todo"])


def test_put_todo_unauthorized(client):
    res = client.put(url_for("todo_resource", id=2))
    assert res.status_code == 401
    assert res.json == {"msg": "Missing Authorization Header"}


def test_put_todo_not_found(client, user_token):
    res = client.put(url_for("todo_resource", id=22), headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert res.status_code == 404
    assert res.json == {
        "message": "Todo not found. You have requested this URI " +
                   "[/todo/22] but did you mean /todo/<int:id> or /todo ?"
    }


def test_put_todo_success(client, user_token):
    res = client.put(url_for("todo_resource", id=2), headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert res.status_code == 200
    assert "completed_todo" in res.json
    TodoUtil.todo_shape.validate(res.json["completed_todo"])


def test_delete_todo_unauthorized(client):
    res = client.delete(url_for("todo_resource", id=2))
    assert res.status_code == 401
    assert res.json == {"msg": "Missing Authorization Header"}


def test_delete_todo_not_found(client, user_token):
    res = client.delete(url_for("todo_resource", id=22), headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert res.status_code == 404
    assert res.json == {
        "message": "Todo not found. You have requested this URI " +
                   "[/todo/22] but did you mean /todo/<int:id> or /todo ?"
    }


def test_delete_todo_success(client, user_token):
    res = client.delete(url_for("todo_resource", id=2), headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert res.status_code == 200
    assert "deleted_todo" in res.json
    TodoUtil.todo_shape.validate(res.json["deleted_todo"])
