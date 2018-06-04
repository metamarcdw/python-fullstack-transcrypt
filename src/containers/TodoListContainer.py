from Component_py.stubs import require  # __:skip
from actions.actions import fetch_all_todos
from components.TodoList import TodoList
connect = require("react-redux").connect


def mapStateToProps(state):
    return {
        "todos": state["todo_list"]
    }


TodoListContainer = connect(
    mapStateToProps
)(TodoList)
