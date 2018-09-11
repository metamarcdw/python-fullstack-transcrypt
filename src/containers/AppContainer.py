from Component_py.stubs import require  # __:skip
from Component_py.component import destruct
from components.App import App
connect = require("react-redux").connect


def mapStateToProps(state):
    text, logged_in = destruct(state["login_user"], "text", "logged_in")
    return {
        "text": text,
        "logged_in": logged_in
    }


AppContainer = connect(
    mapStateToProps
)(App)
