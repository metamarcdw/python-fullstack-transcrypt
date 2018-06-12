from Component_py.stubs import Object  # __:skip
from Component_py.component import destruct
from actions.types import LOGIN_FORM_UPDATE

initial_state = {
    "username_text": "",
    "password_text": ""
}


def login_form_reducer(state=initial_state, action=None):
    type_ = action["type"]
    if type_ == LOGIN_FORM_UPDATE:
        return Object.assign({}, state, action["payload"])

    return state
