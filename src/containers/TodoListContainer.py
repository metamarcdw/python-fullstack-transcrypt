from Component_py.stubs import require  # __:skip
from Component_py.component import destruct
from actions.actions import fetch_all_todos, complete_todo, delete_todo
from components.TodoList import TodoList
connect = require("react-redux").connect


def mapStateToProps(state):
    todos, loading, error = destruct(state["todo_list"],
        "todos", "loading", "error")
    return {
        "token": state.login_user["token"],
        "todos": todos,
        "loading": loading,
        "error": error
    }


def mapDispatchToProps(dispatch):
    return {
        "fetch_all_todos": lambda t: dispatch(fetch_all_todos(t)),
        "complete_todo": lambda i, t: dispatch(complete_todo(i, t)),
        "delete_todo": lambda i, t: dispatch(delete_todo(i, t))
    }


TodoListContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(TodoList)
