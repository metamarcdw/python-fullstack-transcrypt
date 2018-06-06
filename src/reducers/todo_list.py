from Component_py.stubs import Object  # __:skip
from actions.types import (
    FETCH_ALL_TODOS_PENDING, FETCH_ALL_TODOS_FULFILLED, FETCH_ALL_TODOS_REJECTED,
    ADD_NEW_TODO_PENDING, ADD_NEW_TODO_FULFILLED, ADD_NEW_TODO_REJECTED
)


initial_state = {
    "loading": False,
    "todos": [],
    "error": None
}


def todo_list_reducer(state=initial_state, action=None):
    type_ = action["type"]
    if type_ in (FETCH_ALL_TODOS_PENDING, ADD_NEW_TODO_PENDING):
        return Object.assign({}, state, {
            "loading": True
        })
    elif type_ == FETCH_ALL_TODOS_FULFILLED:
        return Object.assign({}, state, {
            "loading": False,
            "todos": action.payload.data["todos"]
        })
    elif type_ in (FETCH_ALL_TODOS_REJECTED, ADD_NEW_TODO_REJECTED):
        msg = action.payload.response.data["message"]
        if not msg:
            msg = "Unknown Error."
        return Object.assign({}, state, {
            "loading": False,
            "error": msg
        })

    elif type_ == ADD_NEW_TODO_FULFILLED:
        new_todo = action.payload.data["new_todo"]
        return Object.assign({}, state, {
            "todos": state["todos"].concat(new_todo)
        })

    return state
