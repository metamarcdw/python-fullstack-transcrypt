from Component_py.stubs import require, __pragma__  # __:skip
from Component_py.component import Component, destruct

React = require("react")
PropTypes = require("prop-types")
Form, FormGroup, Label, Input, Button = destruct(
    require("reactstrap"), "Form", "FormGroup", "Label", "Input", "Button")


class LoginForm(Component):
    propTypes = {
        "username_text": PropTypes.string,
        "password_text": PropTypes.string,
        "login_form_update": PropTypes.func.isRequired,
        "clear_login_form": PropTypes.func.isRequired,
        "login_user": PropTypes.func.isRequired,
        "register_user": PropTypes.func.isRequired
    }

    def on_input_change(self, e):
        self.props.login_form_update(e.target.id, e.target.value)

    def on_submit_login(self, e):
        username, password, clear_login_form, login_user = destruct(
            self.props, "username_text", "password_text", "clear_login_form", "login_user")
        clear_login_form()
        login_user(username, password)
        e.preventDefault()

    def on_click_register(self, e):
        username, password, clear_login_form, register_user = destruct(
            self.props, "username_text", "password_text", "clear_login_form", "register_user")
        clear_login_form()
        register_user(username, password)

    def render(self):
        username_text, password_text = destruct(
            self.props, "username_text", "password_text")
        required = True

        return __pragma__("xtrans", None, "{}", """ (
            <Form className="p-4" onSubmit={self.on_submit_login}>
                <FormGroup>
                    <Label for="username_text">Enter your username</Label>
                    <Input
                        className="no-shadow"
                        onChange={self.on_input_change}
                        value={username_text}
                        placeholder="Your Username"
                        id="username_text"
                        required={required} />
                </FormGroup>
                <FormGroup>
                    <Label for="password_text">Enter your password</Label>
                    <Input
                        className="no-shadow"
                        onChange={self.on_input_change}
                        value={password_text}
                        type="password"
                        id="password_text"
                        required={required} />
                </FormGroup>
                <Button
                    className="fixed-height ml-2 mr-4"
                    type="submit"
                >Login</Button>
                <Button
                    className="fixed-height"
                    onClick={self.on_click_register}
                >Register</Button>
            </Form>
        ); """)
