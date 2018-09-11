from Component_py.component import Component, destruct
from Component_py.stubs import require, __pragma__  # __:skip

React = require("react")
Button = require("reactstrap").Button


class ButtonPanel(Component):
    def on_click_add(self):
        todo_text = self.props.form_panel["text"]
        token = self.props.login_user["token"]
        if todo_text:
            self.props.add_new_todo(todo_text, token)
            self.props.form_panel_update("")

    def on_click_clear(self):
        todo_text = self.props.form_panel["text"]
        if todo_text:
            self.props.form_panel_update("")

    def on_click_logout(self):
        self.on_click_clear()
        self.props.logout_user()

    def render(self):
        return __pragma__("xtrans", None, "{}", """ (
            <div className="d-flex justify-content-center align-items-center">
                <div className="d-flex justify-content-around width-80">
                    <Button
                        className="fixed-height"
                        onClick={self.on_click_add}
                        color="success"
                        type="submit"
                    >Add Todo</Button>
                    <Button
                        className="fixed-height"
                        onClick={self.on_click_clear}
                        color="warning"
                    >Clear Text</Button>
                    <Button
                        className="fixed-height"
                        onClick={self.on_click_logout}
                    >Logout</Button>
                </div>
            </div>
        ); """)
