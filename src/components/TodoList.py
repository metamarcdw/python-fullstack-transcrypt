from Component_py.component import Component, destruct
from Component_py.stubs import require, __pragma__, window  # __:skip

React = require("react")
ListGroup, ListGroupItem, Button = destruct(
    require("reactstrap"), "ListGroup", "ListGroupItem", "Button")
RingLoader = require("react-spinners").RingLoader
FontAwesomeIcon = require("react-fontawesome")


class TodoList(Component):
    def componentDidMount(self):
        self.props.fetch_all_todos(self.props["token"])

    def on_click_complete(self, todo):
        token, complete_todo = destruct(self.props, "token", "complete_todo")
        def closure():
            if not todo["complete"]:
                complete_todo(todo["id"], token)
        return closure

    def on_click_delete(self, todo):
        token, delete_todo = destruct(self.props, "token", "delete_todo")
        def closure():
            if todo["complete"] or window.confirm('Delete incomplete Todo?'):
                delete_todo(todo["id"], token)
        return closure

    def render_spinner(self):
        if not self.props["loading"]:
            return None

        loading = True
        return __pragma__("xtrans", None, "{}", """ (
            <div className="d-flex justify-content-center align-items-center">
                <RingLoader
                    color="#999"
                    size={42}
                    loading={loading} />
                Loading..
            </div>
        ); """)

    def render_checkmark(self, todo):
        if not todo["complete"]:
            return None

        return __pragma__("xtrans", None, "{}", """ (
            <div className="d-flex flex-column justify-content-center align-items-center margin">
                <FontAwesomeIcon
                    name="check-circle"
                    size="2x"
                    className="green-text" />
            </div>
        ); """)

    def render_list_item(self, todo):
        return __pragma__("xtrans", None, "{}", """ (
            <ListGroupItem
                className="d-flex justify-content-center align-items-center"
                key={todo.id}
            >
                {self.render_checkmark(todo)}
                <div className="d-flex flex-grow-1 font-lg">
                    {todo.text}
                </div>
                <Button
                    className="fixed-height margin"
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
        todos, error = destruct(self.props, "todos", "error")
        list_items = map(self.render_list_item, todos)

        return __pragma__("xtrans", None, "{}", """ (
            <div>
                <ListGroup>
                    {list_items}
                </ListGroup>
                <span className="red-text">{error}</span>
                {self.render_spinner()}
            </div>
        ); """)
