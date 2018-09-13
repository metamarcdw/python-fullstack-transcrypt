from Component_py.stubs import Object  # __:skip
from actions.types import (
    FETCH_ALL_TODOS_PENDING, FETCH_ALL_TODOS_FULFILLED, FETCH_ALL_TODOS_REJECTED,
    ADD_NEW_TODO_FULFILLED, ADD_NEW_TODO_REJECTED,
    COMPLETE_TODO_FULFILLED, COMPLETE_TODO_REJECTED,
    DELETE_TODO_FULFILLED, DELETE_TODO_REJECTED
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
            "loading": True,
            "todos": [],
            "error": None
        })

    elif type_ in (ADD_NEW_TODO_REJECTED, COMPLETE_TODO_REJECTED,
                   DELETE_TODO_REJECTED):
        response = action.payload["response"] or None
        data = response["data"] if response and response["data"] else None
        msg = data["message"] if data and data["message"] else "Unknown Error."
        return Object.assign({}, state, {
            "loading": False,
            "error": msg
        })

    elif type_ == FETCH_ALL_TODOS_REJECTED:
        mutation = {
            "loading": False,
            "todos": []
        }
        response = action.payload["response"] or None
        data = response["data"] if response and response["data"] else None
        msg = data["message"] if data and data["message"] else "Unknown Error."

        if "No todos found." not in msg:
            mutation["error"] = msg
        return Object.assign({}, state, mutation)

    elif type_ == FETCH_ALL_TODOS_FULFILLED:
        return Object.assign({}, state, {
            "loading": False,
            "todos": action.payload.data["todos"]
        })

    elif type_ == ADD_NEW_TODO_FULFILLED:
        new_todo = action.payload.data["new_todo"]
        return Object.assign({}, state, {
            "loading": False,
            "todos": state["todos"].concat(new_todo),
            "error": None
        })

    elif type_ == COMPLETE_TODO_FULFILLED:
        completed_todo = action.payload.data["completed_todo"]

        def complete(todo):
            if todo["id"] == completed_todo["id"]:
                todo["complete"] = True
            return todo

        return Object.assign({}, state, {
            "loading": False,
            "todos": map(complete, state["todos"])
        })

    elif type_ == DELETE_TODO_FULFILLED:
        deleted_todo = action.payload.data["deleted_todo"]
        return Object.assign({}, state, {
            "loading": False,
            "todos": filter(lambda t: t["id"] != deleted_todo["id"], state["todos"])
        })

    return state
