from Component_py.stubs import require, __pragma__  # __:skip
from Component_py.component import Component, destruct

React = require("react")
ListGroup, ListGroupItem, Button = destruct(
    require("reactstrap"), "ListGroup", "ListGroupItem", "Button")
RingLoader = require("react-spinners").RingLoader
FontAwesomeIcon = require("react-fontawesome")


class TodoList(Component):
    def componentDidMount(self):
        token = self.props.login_user["token"]
        self.props.fetch_all_todos(token)

    def on_click_complete(self, todo):
        token = self.props.login_user["token"]

        def closure():
            if not todo["complete"]:
                self.props.complete_todo(todo["id"], token)
        return closure

    def on_click_delete(self, todo):
        token = self.props.login_user["token"]
        return lambda: self.props.delete_todo(todo["id"], token)

    def render_spinner(self):
        loading = True
        return __pragma__("xtrans", None, "{}", """ (
            <div className="flex-center">
                <RingLoader
                    color="#999"
                    loading={loading} />
            </div>
        ); """)

    def render_checkmark(self, todo):
        if todo["complete"]:
            return __pragma__("xtrans", None, "{}", """ (
                <div className="flex-column flex-center margin">
                    <FontAwesomeIcon
                        name="check-circle"
                        size="2x"
                        className="green-text" />
                </div>
            ); """)
        return None

    def render_list_item(self, todo):
        return __pragma__("xtrans", None, "{}", """ (
            <ListGroupItem
                className="flex-center"
                key={todo.id}
            >
                {self.render_checkmark(todo)}
                <div className="list-item">
                    {todo.text}
                </div>
                <Button
                    className="margin"
                    color="primary"
                    onClick={self.on_click_complete(todo)}
                >Complete</Button>
                <Button
                    color="danger"
                    onClick={self.on_click_delete(todo)}
                >Delete</Button>
            </ListGroupItem>
        ); """)

    def render(self):
        todo_list = self.props["todo_list"]
        if todo_list["loading"]:
            return self.render_spinner()

        list_items = map(self.render_list_item, todo_list["todos"])
        return __pragma__("xtrans", None, "{}", """ (
            <div>
                <ListGroup>
                    {list_items}
                </ListGroup>
                <span className="red-text">{todo_list.error}</span>
            </div>
        ); """)
