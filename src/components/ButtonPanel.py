from Component_py.stubs import require, __pragma__  # __:skip
React = require("react")
Button = require("reactstrap").Button


def ButtonPanel(props):
    def on_click_add():
        todo_text = props.form_panel["text"]
        token = props.login_user["token"]
        if todo_text:
            props.add_new_todo(todo_text, token)
            props.form_panel_update("")

    def on_click_clear():
        todo_text = props.form_panel["text"]
        if todo_text:
            props.form_panel_update("")

    return __pragma__("xtrans", None, "{}", """ (
        <div className="flex-center">
            <div className="flex-container">
                <Button
                    onClick={on_click_add}
                    color="success"
                >Add Todo</Button>
                <Button
                    onClick={on_click_clear}
                    color="warning"
                >Clear Text</Button>
            </div>
        </div>
    ); """)
