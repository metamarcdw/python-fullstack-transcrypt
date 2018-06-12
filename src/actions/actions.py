from Component_py.stubs import require, console  # __:skip
from actions.types import (
    FETCH_ALL_TODOS, COMPLETE_TODO, DELETE_TODO, ADD_NEW_TODO,
    REGISTER_USER, REGISTER_USER_REJECTED, LOGIN_USER, LOGOUT_USER,
    FORM_PANEL_UPDATE, LOGIN_FORM_UPDATE
)
axios = require("axios").create({"baseURL": "https://metamarcdw.pythonanywhere.com"})


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
        "payload": axios.delete(f"/todo/{id_}", bearer(token))
    }


def add_new_todo(text, token):
    new_todo = {"text": text}
    return {
        "type": ADD_NEW_TODO,
        "payload": axios.post("/todo", new_todo, bearer(token))
    }


def register_user(username, password):
    new_user = {
        "name": username,
        "password": password
    }
    def thunk(dispatch):
        axios.post("/user", new_user)\
            .then(lambda json: dispatch(login_user(username, password)))\
            .catch(lambda err: dispatch({
                "type": REGISTER_USER_REJECTED,
                "payload": err
            }))
    return thunk


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


def logout_user():
    return {
        "type": LOGOUT_USER
    }


def form_panel_update(todo_text):
    return {
        "type": FORM_PANEL_UPDATE,
        "payload": {
            "text": todo_text
        }
    }


def login_form_update(field_name, field_text):
    return {
        "type": LOGIN_FORM_UPDATE,
        "payload": {
            field_name: field_text
        }
    }
