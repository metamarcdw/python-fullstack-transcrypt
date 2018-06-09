from Component_py.stubs import require  # __:skip
from actions.actions import add_new_todo, form_panel_update, logout_user
from components.ButtonPanel import ButtonPanel
connect = require("react-redux").connect


def mapStateToProps(state):
    return {
        "login_user": state["login_user"],
        "form_panel": state["form_panel"]
    }


def mapDispatchToProps(dispatch):
    return {
        "add_new_todo": lambda tx, to: dispatch(add_new_todo(tx, to)),
        "form_panel_update": lambda t: dispatch(form_panel_update(t)),
        "logout_user": lambda: dispatch(logout_user())
    }


ButtonPanelContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(ButtonPanel)
