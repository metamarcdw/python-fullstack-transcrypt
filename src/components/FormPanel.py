from Component_py.stubs import require, __pragma__  # __:skip
from Component_py.component import Component, destruct

React = require("react")
PropTypes = require("prop-types")
FormGroup, Label, Input = destruct(
    require("reactstrap"), "FormGroup", "Label", "Input")


class FormPanel(Component):
    propTypes = {
        "text": PropTypes.string,
        "form_panel_update": PropTypes.func.isRequired
    }

    def on_text_change(self, e):
        self.props.form_panel_update(e.target.value)

    def render(self):
        required = True
        return __pragma__("xtrans", None, "{}", """ (
            <FormGroup>
                <Label for="text_input">Enter new todo text:</Label>
                <Input
                    onChange={self.on_text_change}
                    value={self.props.text}
                    id="text_input"
                    placeholder="What to do?" />
            </FormGroup>
        ); """)
