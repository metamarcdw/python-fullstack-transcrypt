from Component_py.stubs import Object, console  # __:skip
from actions.types import FORM_PANEL_UPDATE


initial_state = {
    "text": ""
}


def form_panel_reducer(state=initial_state, action=None):
    type_ = action["type"]
    if type_ == FORM_PANEL_UPDATE:
        return Object.assign({}, state, action["payload"])
    return state
