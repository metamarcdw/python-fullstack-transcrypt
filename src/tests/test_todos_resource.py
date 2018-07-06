import json
from flask import url_for
from server.routes import TodoUtil


def test_get_all_todos_unauthorized(client):
    res = client.get(url_for("todos_resource"))
    assert res.status_code == 401
    assert res.json == {"msg": "Missing Authorization Header"}


def test_get_all_todos_none_found(client, admin_token):
    res = client.get(url_for("todos_resource"), headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert res.status_code == 404
    assert res.json == {
        "message": "No todos found. You have requested this URI " +
                   "[/todo] but did you mean /todo or /todo/<int:id> ?"
    }


def test_get_all_todos_success(client, user_token):
    res = client.get(url_for("todos_resource"), headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert res.status_code == 200
    assert "todos" in res.json
    todos = res.json["todos"]
    assert todos
    for todo in todos:
        TodoUtil.todo_shape.validate(todo)


def test_post_todo_malformed(client):
    res = client.post(url_for("todos_resource"),
                      content_type="application/json",
                      data=json.dumps({
                          "something": "wrong"
                      }))
    assert res.status_code == 400
    assert "message" in res.json
    assert res.json["message"] == "Input payload validation failed"


def test_post_todo_unauthorized(client):
    res = client.post(url_for("todos_resource"),
                      content_type="application/json",
                      data=json.dumps({
                          "text": "testing.."
                      }))
    assert res.status_code == 401
    assert res.json == {"msg": "Missing Authorization Header"}


def test_post_todo_success(client, user_token):
    res = client.post(url_for("todos_resource"),
                      content_type="application/json",
                      data=json.dumps({
                          "text": "testing.."
                      }),
                      headers={
                          "Authorization": f"Bearer {user_token}"
                      })
    assert res.status_code == 200
    assert "new_todo" in res.json
    TodoUtil.todo_shape.validate(res.json["new_todo"])
