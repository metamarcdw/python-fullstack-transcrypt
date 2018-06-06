from Component_py.stubs import require, __pragma__, console  # __:skip
from Component_py.component import Component, destruct

React = require("react")
ListGroup, ListGroupItem, Button = destruct(
    require("reactstrap"), "ListGroup", "ListGroupItem", "Button")
RingLoader = require("react-spinners").RingLoader


class TodoList(Component):
    def componentWillMount(self):
        self.props.fetch_all_todos(self.props.login_user["token"])

    def on_click_complete(self, todo_id):
        return lambda: console.log(todo_id)

    def on_click_delete(self, todo_id):
        return lambda: console.log(todo_id)

    def render(self):
        def render_list_item(todo):
            return __pragma__("xtrans", None, "{}", """ (
                <ListGroupItem
                    className="flex-center"
                    key={todo.id}
                >
                    <div className="list-item">
                        {todo.text}
                    </div>
                    <Button
                        color="primary"
                        onClick={self.on_click_complete(todo.id)}
                    >Complete</Button>
                    <Button
                        color="danger"
                        onClick={self.on_click_delete(todo.id)}
                    >Delete</Button>
                </ListGroupItem>
            ); """)

        if self.props.todo_list["loading"]:
            loading = True
            return __pragma__("xtrans", None, "{}", """ (
                <div className="flex-center">
                    <RingLoader
                        color={"#999"}
                        loading={loading}
                    />
                </div>
            ); """)

        list_items = map(render_list_item, self.props.todo_list["todos"])
        return __pragma__("xtrans", None, "{}", """ (
            <ListGroup>
                {list_items}
            </ListGroup>
        ); """)
