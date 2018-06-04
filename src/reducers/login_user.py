from Component_py.stubs import Object  # __:skip
from actions.types import (
    LOGIN_USER_PENDING, LOGIN_USER_FULFILLED, LOGIN_USER_REJECTED
)


initial_state = {
    "loading": False,
    "logged_in": False,
    "token": None,
    "error": None
}


def login_user_reducer(state=initial_state, action=None):
    type_ = action["type"]
    if type_ == LOGIN_USER_PENDING:
        return Object.assign({}, state, {
            "loading": True,
            "error": None
        })
    elif type_ == LOGIN_USER_FULFILLED:
        return Object.assign({}, state, {
            "loading": False,
            "logged_in": True,
            "token": action.payload.data["token"]
        })
    elif type_ == LOGIN_USER_REJECTED:
        msg = action.payload.response.data["message"]
        if not msg:
            msg = "Unknown Error."
        return Object.assign({}, state, {
            "loading": False,
            "error": msg
        })
    return state
