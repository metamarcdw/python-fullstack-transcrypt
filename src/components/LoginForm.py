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

    return __pragma__("xtrans", None, "{}", """ (
        <Form className="padding">
            <FormGroup>
                <Label for="username_input">Enter your username</Label>
                <Input
                    onChange={on_username_change}
                    value={props.data.username_text}
                    placeholder="Your Username"
                    id="username_input"
                />
            </FormGroup>
            <FormGroup>
                <Label for="password_input">Enter your password</Label>
                <Input
                    onChange={on_password_change}
                    value={props.data.password_text}
                    type="password"
                    id="password_input"
                />
            </FormGroup>
            <Button
                onClick={props.on_click}
            >Login</Button>
        </Form>
    ); """)
