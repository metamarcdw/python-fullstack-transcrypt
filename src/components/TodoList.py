from Component_py.stubs import require, __pragma__, console  # __:skip
from Component_py.component import Component, destruct

React = require("react")
ListGroup, ListGroupItem, Button = destruct(
    require("reactstrap"), "ListGroup", "ListGroupItem", "Button")

class TodoList(Component):
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

        list_items = map(render_list_item, self.props["todos"])
        return __pragma__("xtrans", None, "{}", """ (
            <ListGroup>
                {list_items}
            </ListGroup>
        ); """)
