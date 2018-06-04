from Component_py.stubs import Object  # __:skip
from actions.types import (
    FETCH_ALL_TODOS_PENDING, FETCH_ALL_TODOS_FULFILLED,
    FETCH_ALL_TODOS_REJECTED
)


initial_state = {
    "loading": False,
    "todos": [],
    "error": None
}


def todo_list_reducer(state=initial_state, action=None):
    type_ = action["type"]
    if type_ == FETCH_ALL_TODOS_PENDING:
        return Object.assign({}, state, {
            "loading": True
        })
    elif type_ == FETCH_ALL_TODOS_FULFILLED:
        return Object.assign({}, state, {
            "loading": False,
            "todos": action.payload.data["todos"]
        })
    elif type_ == FETCH_ALL_TODOS_REJECTED:
        msg = action.payload.response.data["message"]
        if not msg:
            msg = "Unknown Error."
        return Object.assign({}, state, {
            "loading": False,
            "error": msg
        })
    return state
