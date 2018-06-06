from Component_py.stubs import require, __pragma__  # __:skip
React = require("react")
Button = require("reactstrap").Button


def ButtonPanel(props):
    def on_click_add():
        todo_text = props.form_panel["text"]
        token = props.login_user["token"]
        if todo_text:
            props.add_new_todo(todo_text, token)
            props.clear_form_panel()

    return __pragma__("xtrans", None, "{}", """ (
        <div className="flex-center">
            <div className="flex-container">
                <Button
                    onClick={on_click_add}
                    color="success"
                >Add Todo</Button>
                <Button
                    onClick={props.clear_form_panel}
                    color="warning"
                >Clear Text</Button>
            </div>
        </div>
    ); """)
