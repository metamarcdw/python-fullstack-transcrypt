from Component_py.stubs import require  # __:skip
from actions.actions import form_panel_update
from components.FormPanel import FormPanel
connect = require("react-redux").connect


def mapStateToProps(state):
    return {
        "text": state.form_panel["text"]
    }


def mapDispatchToProps(dispatch):
    return {
        "form_panel_update": lambda t: dispatch(form_panel_update(t))
    }


FormPanelContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(FormPanel)
