from Component_py.stubs import Object  # __:skip
from actions.types import (
    FETCH_ALL_TODOS_PENDING, FETCH_ALL_TODOS_FULFILLED,
    FETCH_ALL_TODOS_REJECTED
)


initial_state = {
    "todos": []
}


def todo_list_reducer(state=initial_state, action=None):
    type_ = action["type"]
    if type_ == FETCH_ALL_TODOS_PENDING:
        return state
    elif type_ == FETCH_ALL_TODOS_FULFILLED:
        return Object.assign({}, state, {
            "todos": action.payload.data["todos"]
        })
    elif type_ == FETCH_ALL_TODOS_REJECTED:
        return state
    return state
