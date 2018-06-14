from Component_py.stubs import require, __pragma__  # __:skip
from Component_py.component import destruct

React = require("react")
Form, FormGroup, Label, Input = destruct(
    require("reactstrap"), "Form", "FormGroup", "Label", "Input")


def FormPanel(props):
    def on_text_change(e):
        props.form_panel_update(e.target.value)

    return __pragma__("xtrans", None, "{}", """ (
        <Form className="padding">
            <FormGroup>
                <Label for="text_input">Enter new todo text:</Label>
                <Input
                    onChange={on_text_change}
                    value={props.data.text}
                    id="text_input"
                    placeholder="What to do?" />
            </FormGroup>
        </Form>
    ); """)
