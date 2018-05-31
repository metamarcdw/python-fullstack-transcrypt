from Component_py.component import destruct
from actions.types import LOGIN_FORM_UPDATE

initial_state = {
    "username_text": "",
    "password_text": ""
}


def login_form_reducer(state=initial_state, action=None):
    type_ = action["type"]
    if type_ == LOGIN_FORM_UPDATE:
        old_username, old_password = destruct(
            state, "username_text", "password_text")
        new_username, new_password = destruct(
            action["payload"], "username_text", "password_text")
        user = new_username if new_username is not None else old_username
        pswd = new_password if new_password is not None else old_password
        return {
            "username_text": user,
            "password_text": pswd
        }

    return state
