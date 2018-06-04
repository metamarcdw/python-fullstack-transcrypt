from Component_py.stubs import require, __pragma__, console  # __:skip
React = require("react")
Button = require("reactstrap").Button


def ButtonPanel(props):
    def on_click_add():
        todo_text = props.form_panel["text"]
        token = props.login_user["token"]
        if todo_text and token:
            console.log(f"TEXT: {todo_text}\nTOKEN: {token}")
            props.add_new_todo(todo_text, token)

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
