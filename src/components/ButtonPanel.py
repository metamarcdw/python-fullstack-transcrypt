from Component_py.stubs import require, __pragma__  # __:skip
from Component_py.component import Component, destruct

React = require("react")
PropTypes = require("prop-types")
Button = require("reactstrap").Button


class ButtonPanel(Component):
    propTypes = {
        "text": PropTypes.string,
        "token": PropTypes.string.isRequired,
        "add_new_todo": PropTypes.func.isRequired,
        "form_panel_update": PropTypes.func.isRequired,
        "logout_user": PropTypes.func.isRequired
    }

    def on_click_add(self):
        text, token, form_panel_update, add_new_todo = destruct(
            self.props, "text", "token", "form_panel_update", "add_new_todo")
        if text:
            add_new_todo(text, token)
            form_panel_update("")

    def on_click_clear(self):
        text, form_panel_update = destruct(
            self.props, "text", "form_panel_update")
        if text:
            form_panel_update("")

    def on_click_logout(self):
        self.on_click_clear()
        self.props.logout_user()

    def render(self):
        return __pragma__("xtrans", None, "{}", """ (
            <div className="d-flex justify-content-center align-items-center">
                <div className="d-flex justify-content-around w-75">
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
