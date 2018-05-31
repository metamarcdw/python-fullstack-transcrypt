from Component_py.stubs import require, __pragma__, console  # __:skip
from Component_py.component import Component, destruct

React = require("react")
ListGroup, ListGroupItem, Button = destruct(
    require("reactstrap"), "ListGroup", "ListGroupItem", "Button")


class TodoList(Component):
    def on_click(self, todo_id):
        return lambda: console.log(todo_id)

    def render(self):
        def render_list(todo):
            return __pragma__("xtrans", None, "{}", """ (
                <ListGroupItem
                    className="flex-center"
                    key={todo.id}
                >
                    <div className="list-item">
                        {todo.text}
                    </div>
                    <Button
                        color="danger"
                        onClick={self.on_click(todo.id)}
                    >Delete</Button>
                </ListGroupItem>
            ); """)
        list_items = map(render_list, self.props["todos"])

        return __pragma__("xtrans", None, "{}", """ (
            <ListGroup>
                {list_items}
            </ListGroup>
        ); """)
