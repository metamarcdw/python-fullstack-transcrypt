from Component_py.stubs import require, __pragma__, document  # __:skip
from components.App import App

React = require("react")
ReactDOM = require("react-dom")

app = __pragma__("xtrans", None, "<App />")
ReactDOM.render(app, document.getElementById("root"))
