from Component_py.stubs import require  # __:skip
from Component_py.component import destruct
from components.App import App
connect = require("react-redux").connect


def mapStateToProps(state):
    logged_in, loading, error = destruct(
        state["login_user"], "logged_in", "loading", "error")
    return {
        "logged_in": logged_in,
        "loading": loading,
        "error": error
    }


AppContainer = connect(
    mapStateToProps
)(App)
