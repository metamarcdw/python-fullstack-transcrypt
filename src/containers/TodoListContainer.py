from Component_py.stubs import require  # __:skip
from actions.actions import fetch_all_todos
from components.TodoList import TodoList
connect = require("react-redux").connect


def mapStateToProps(state):
    return {
        "todo_list": state["todo_list"],
        "login_user": state["login_user"]
    }


def mapDispatchToProps(dispatch):
    return {
        "fetch_all_todos": lambda t: dispatch(fetch_all_todos(t))
    }


TodoListContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(TodoList)
