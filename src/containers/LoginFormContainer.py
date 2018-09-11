from Component_py.stubs import require  # __:skip
from Component_py.component import destruct
from actions.actions import (
    login_form_update, clear_login_form, login_user, register_user
)
from components.LoginForm import LoginForm
connect = require("react-redux").connect


def mapStateToProps(state):
    username_text, password_text = destruct(state["login_form"],
        "username_text", "password_text")
    return {
        "username_text": username_text,
        "password_text": password_text
    }


def mapDispatchToProps(dispatch):
    return {
        "login_form_update": lambda u, p: dispatch(login_form_update(u, p)),
        "clear_login_form": lambda: dispatch(clear_login_form()),
        "login_user": lambda u, p: dispatch(login_user(u, p)),
        "register_user": lambda u, p: dispatch(register_user(u, p))
    }


LoginFormContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(LoginForm)
