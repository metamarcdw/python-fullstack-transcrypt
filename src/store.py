from Component_py.stubs import require, __pragma__  # __:skip
from Component_py.component import destruct

from reducers.todo_list import todo_list_reducer
from reducers.login_user import login_user_reducer
from reducers.login_form import login_form_reducer
from reducers.form_panel import form_panel_reducer

createStore, combineReducers, applyMiddleware = destruct(
    require("redux"), "createStore", "combineReducers", "applyMiddleware")

logger = require("redux-logger").createLogger
promise = require("redux-promise-middleware").js_default
thunk = require("redux-thunk").js_default

store = createStore(
    combineReducers({
        "todo_list": todo_list_reducer,
        "login_user": login_user_reducer,
        "login_form": login_form_reducer,
        "form_panel": form_panel_reducer
    }),
    applyMiddleware(
        logger(),
        promise(),
        thunk
    )
)
