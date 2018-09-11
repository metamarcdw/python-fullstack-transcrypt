from Component_py.component import Component, destruct
from Component_py.stubs import require, __pragma__  # __:skip

React = require("react")
Form, FormGroup, Label, Input, Button = destruct(
    require("reactstrap"), "Form", "FormGroup", "Label", "Input", "Button")


class LoginForm(Component):
    def on_input_change(self, e):
        self.props.login_form_update(e.target.id, e.target.value)

    def on_submit_login(self, e):
        username, password, clear_login_form, login_user = destruct(self.props,
            "username_text", "password_text", "clear_login_form", "login_user")
        if username and password:
            clear_login_form()
            login_user(username, password)
        e.preventDefault()

    def on_click_register(self, e):
        username, password, clear_login_form, register_user = destruct(self.props,
            "username_text", "password_text", "clear_login_form", "register_user")
        if username and password:
            clear_login_form()
            register_user(username, password)

    def render(self):
        username_text, password_text = destruct(self.props,
            "username_text", "password_text")

        return __pragma__("xtrans", None, "{}", """ (
            <Form className="padding" onSubmit={self.on_submit_login}>
                <FormGroup>
                    <Label for="username_text">Enter your username</Label>
                    <Input
                        onChange={self.on_input_change}
                        value={username_text}
                        placeholder="Your Username"
                        id="username_text" />
                </FormGroup>
                <FormGroup>
                    <Label for="password_text">Enter your password</Label>
                    <Input
                        onChange={self.on_input_change}
                        value={password_text}
                        type="password"
                        id="password_text" />
                </FormGroup>
                <Button
                    className="fixed-height margin"
                    type="submit"
                >Login</Button>
                <Button
                    className="fixed-height"
                    onClick={self.on_click_register}
                >Register</Button>
            </Form>
        ); """)
