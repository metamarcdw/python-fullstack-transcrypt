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

    def on_click_logout():
        on_click_clear()
        props.logout_user()

    return __pragma__("xtrans", None, "{}", """ (
        <div className="d-flex justify-content-center align-items-center">
            <div className="d-flex justify-content-around width-80">
                <Button
                    className="fixed-height"
                    onClick={on_click_add}
                    color="success"
                    type="submit"
                >Add Todo</Button>
                <Button
                    className="fixed-height"
                    onClick={on_click_clear}
                    color="warning"
                >Clear Text</Button>
                <Button
                    className="fixed-height"
                    onClick={on_click_logout}
                >Logout</Button>
            </div>
        </div>
    ); """)
