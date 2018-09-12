from Component_py.stubs import require, __pragma__, window  # __:skip
from Component_py.component import Component, destruct
from components.Spinner import Spinner

React = require("react")
PropTypes = require("prop-types")
ListGroup, ListGroupItem, Button = destruct(
    require("reactstrap"), "ListGroup", "ListGroupItem", "Button")
FontAwesomeIcon = require("react-fontawesome")


class TodoList(Component):
    propTypes = {
        "token": PropTypes.string.isRequired,
        "todos": PropTypes.array.isRequired,
        "loading": PropTypes.bool.isRequired,
        "error": PropTypes.string,
        "fetch_all_todos": PropTypes.func.isRequired,
        "complete_todo": PropTypes.func.isRequired,
        "delete_todo": PropTypes.func.isRequired
    }

    def componentDidMount(self):
        token, fetch_all_todos = destruct(
            self.props, "token", "fetch_all_todos")
        fetch_all_todos(token)

    def on_click_complete(self, todo):
        complete, id_ = destruct(todo, "complete", "id")
        token, complete_todo = destruct(self.props, "token", "complete_todo")

        def closure():
            if not complete:
                complete_todo(id_, token)
        return closure

    def on_click_delete(self, todo):
        complete, id_ = destruct(todo, "complete", "id")
        token, delete_todo = destruct(self.props, "token", "delete_todo")

        def closure():
            if complete or window.confirm('Delete incomplete Todo?'):
                delete_todo(id_, token)
        return closure

    def render_checkmark(self, todo):
        if not todo["complete"]:
            return None

        return __pragma__("xtrans", None, "{}", """ (
            <div className="d-flex flex-column justify-content-center align-items-center ml-2 mr-4">
                <FontAwesomeIcon
                    name="check-circle"
                    size="2x"
                    className="text-success" />
            </div>
        ); """)

    def render_list_item(self, todo):
        return __pragma__("xtrans", None, "{}", """ (
            <ListGroupItem
                className="d-flex justify-content-center align-items-center"
                key={todo.id}
            >
                {self.render_checkmark(todo)}
                <div className="d-flex flex-grow-1">
                    <h5>{todo.text}</h5>
                </div>
                <Button
                    className="fixed-height ml-2 mr-4"
                    color="primary"
                    onClick={self.on_click_complete(todo)}
                    disabled={todo.complete}
                >Complete</Button>
                <Button
                    className="fixed-height"
                    color="danger"
                    onClick={self.on_click_delete(todo)}
                >Delete</Button>
            </ListGroupItem>
        ); """)

    def render(self):
        todos, error, loading = destruct(
            self.props, "todos", "error", "loading")
        list_items = map(self.render_list_item, todos)

        return __pragma__("xtrans", None, "{}", """ (
            <div>
                <ListGroup>
                    {list_items}
                </ListGroup>
                <span className="text-danger">{error}</span>
                <Spinner loading={loading} />
            </div>
        ); """)
