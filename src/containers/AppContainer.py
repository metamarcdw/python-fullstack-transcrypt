from Component_py.stubs import require  # __:skip
from components.App import App
connect = require("react-redux").connect


def mapStateToProps(state):
    return {
        "login_user": state["login_user"]
    }


AppContainer = connect(
    mapStateToProps
)(App)
