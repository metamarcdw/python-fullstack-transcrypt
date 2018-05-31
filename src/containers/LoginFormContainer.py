from Component_py.stubs import require  # __:skip
from actions.actions import login_form_update
from components.LoginForm import LoginForm
connect = require("react-redux").connect


def mapStateToProps(state):
    return {"data": state["login_form"]}


def mapDispatchToProps(dispatch):
    return {
        "login_form_update": lambda u, p: dispatch(login_form_update(u, p))
    }


LoginFormContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(LoginForm)
