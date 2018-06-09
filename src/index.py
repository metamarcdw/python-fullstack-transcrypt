from Component_py.stubs import require, __pragma__, document  # __:skip
from containers.AppContainer import AppContainer
from store import store

React = require("react")
ReactDOM = require("react-dom")
Provider = require("react-redux").Provider

app = __pragma__("xtrans", None, "{}", """ (
    <Provider store={store}>
        <AppContainer />
    </Provider>
); """)
ReactDOM.render(app, document.getElementById("root"))
