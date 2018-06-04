from Component_py.stubs import require  # __:skip
from actions.actions import form_panel_update
from components.ButtonPanel import ButtonPanel
connect = require("react-redux").connect


def mapDispatchToProps(dispatch):
    return {
        "clear_form_panel": lambda: dispatch(form_panel_update(""))
    }


ButtonPanelContainer = connect(
    None,
    mapDispatchToProps
)(ButtonPanel)
