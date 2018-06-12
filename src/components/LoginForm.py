from Component_py.stubs import require, __pragma__  # __:skip
from Component_py.component import destruct

React = require("react")
Form, FormGroup, Label, Input, Button = destruct(
    require("reactstrap"), "Form", "FormGroup", "Label", "Input", "Button")


def LoginForm(props):
    def on_input_change(e):
        props.login_form_update(e.target.id, e.target.value)

    def on_click_login(e):
        username, password = destruct(
            props["login_form"], "username_text", "password_text")
        if username and password:
            props.do_login(username, password)
        props.login_form_update("", "")
        e.preventDefault()

    def on_click_register(e):
        username, password = destruct(
            props["login_form"], "username_text", "password_text")
        if username and password:
            props.register_user(username, password)
            props.do_login(username, password)
        props.login_form_update("", "")
        e.preventDefault()

    return __pragma__("xtrans", None, "{}", """ (
        <Form className="padding">
            <FormGroup>
                <Label for="username_text">Enter your username</Label>
                <Input
                    onChange={on_input_change}
                    value={props.login_form.username_text}
                    placeholder="Your Username"
                    id="username_text"
                />
            </FormGroup>
            <FormGroup>
                <Label for="password_text">Enter your password</Label>
                <Input
                    onChange={on_input_change}
                    value={props.login_form.password_text}
                    type="password"
                    id="password_text"
                />
            </FormGroup>
            <Button
                className="margin"
                onClick={on_click_login}
            >Login</Button>
            <Button
                onClick={on_click_register}
            >Register</Button>
        </Form>
    ); """)
