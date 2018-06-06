from Component_py.stubs import require  # __:skip
from actions.types import (
    FETCH_ALL_TODOS, COMPLETE_TODO, DELETE_TODO, ADD_NEW_TODO,
    LOGIN_USER, FORM_PANEL_UPDATE, LOGIN_FORM_UPDATE
)
axios = require("axios").create({"baseURL": "/api"})


def bearer(token):
    return {
        "headers": {
            "Authorization": f"Bearer {token}"
        }
    }


def fetch_all_todos(token):
    return {
        "type": FETCH_ALL_TODOS,
        "payload": axios.js_get("/todo", bearer(token))
    }


def complete_todo(id_, token):
    return {
        "type": COMPLETE_TODO,
        "payload": axios.put(f"/todo/{id_}", None, bearer(token))
    }


def delete_todo(id_, token):
    return {
        "type": DELETE_TODO,
        "payload": axios.delete(f"/todo/{id_}", None, bearer(token))
    }


def add_new_todo(text, token):
    new_todo = {"text": text}
    return {
        "type": ADD_NEW_TODO,
        "payload": axios.post("/todo", new_todo, bearer(token))
    }


def login_user(username, password):
    return {
        "type": LOGIN_USER,
        "payload": axios.js_get("/login", {
            "auth": {
                "username": username,
                "password": password
            }
        })
    }


def form_panel_update(todo_text):
    return {
        "type": FORM_PANEL_UPDATE,
        "payload": {
            "text": todo_text
        }
    }


def login_form_update(username_text, password_text):
    return {
        "type": LOGIN_FORM_UPDATE,
        "payload": {
            "username_text": username_text,
            "password_text": password_text
        }
    }
