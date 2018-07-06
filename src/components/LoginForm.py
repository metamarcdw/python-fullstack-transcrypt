from Component_py.stubs import require, __pragma__  # __:skip
from Component_py.component import destruct

React = require("react")
Form, FormGroup, Label, Input, Button = destruct(
    require("reactstrap"), "Form", "FormGroup", "Label", "Input", "Button")


def LoginForm(props):
    def on_input_change(e):
        props.login_form_update(e.target.id, e.target.value)

    def on_submit_login(e):
        username, password = destruct(
            props["login_form"], "username_text", "password_text")
        if username and password:
            props.clear_login_form()
            props.login_user(username, password)
        e.preventDefault()

    def on_click_register(e):
        username, password = destruct(
            props["login_form"], "username_text", "password_text")
        if username and password:
            props.clear_login_form()
            props.register_user(username, password)

    return __pragma__("xtrans", None, "{}", """ (
        <Form className="padding" onSubmit={on_submit_login}>
            <FormGroup>
                <Label for="username_text">Enter your username</Label>
                <Input
                    onChange={on_input_change}
                    value={props.login_form.username_text}
                    placeholder="Your Username"
                    id="username_text" />
            </FormGroup>
            <FormGroup>
                <Label for="password_text">Enter your password</Label>
                <Input
                    onChange={on_input_change}
                    value={props.login_form.password_text}
                    type="password"
                    id="password_text" />
            </FormGroup>
            <Button
                className="fixed-height margin"
                type="submit"
            >Login</Button>
            <Button
                className="fixed-height"
                onClick={on_click_register}
            >Register</Button>
        </Form>
    ); """)
