from Component_py.stubs import require, __pragma__  # __:skip
from Component_py.component import destruct

React = require("react")
Form, FormGroup, Label, Input, Button = destruct(
    require("reactstrap"), "Form", "FormGroup", "Label", "Input", "Button")


def LoginForm(props):
    def on_username_change(e):
        props.login_form_update(e.target.value, None)

    def on_password_change(e):
        props.login_form_update(None, e.target.value)

    def on_click_login(e):
        username, password = destruct(
            props["login_form"], "username_text", "password_text")
        if username and password:
            props.do_login(username, password)
        e.preventDefault()

    return __pragma__("xtrans", None, "{}", """ (
        <Form className="padding">
            <FormGroup>
                <Label for="username_input">Enter your username</Label>
                <Input
                    onChange={on_username_change}
                    value={props.login_form.username_text}
                    placeholder="Your Username"
                    id="username_input"
                />
            </FormGroup>
            <FormGroup>
                <Label for="password_input">Enter your password</Label>
                <Input
                    onChange={on_password_change}
                    value={props.login_form.password_text}
                    type="password"
                    id="password_input"
                />
            </FormGroup>
            <Button
                onClick={on_click_login}
            >Login</Button>
        </Form>
    ); """)
