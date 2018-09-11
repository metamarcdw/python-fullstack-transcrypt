from Component_py.component import Component, destruct
from Component_py.stubs import require, __pragma__  # __:skip

React = require("react")
FormGroup, Label, Input = destruct(
    require("reactstrap"), "FormGroup", "Label", "Input")


class FormPanel(Component):
    def on_text_change(self, e):
        self.props.form_panel_update(e.target.value)

    def render(self):
        return __pragma__("xtrans", None, "{}", """ (
            <FormGroup>
                <Label for="text_input">Enter new todo text:</Label>
                <Input
                    onChange={self.on_text_change}
                    value={self.props.form_panel.text}
                    id="text_input"
                    placeholder="What to do?" />
            </FormGroup>
        ); """)
