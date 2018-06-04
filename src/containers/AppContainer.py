from Component_py.stubs import require  # __:skip
from actions.actions import login_user
from components.App import App
connect = require("react-redux").connect


def mapStateToProps(state):
    return {
        "login_user": state["login_user"],
        "login_form": state["login_form"]
    }


def mapDispatchToProps(dispatch):
    return {
        "do_login": lambda u, p: dispatch(login_user(u, p))
    }


AppContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(App)
