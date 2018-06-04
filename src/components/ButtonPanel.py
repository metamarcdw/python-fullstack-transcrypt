from Component_py.stubs import require, __pragma__  # __:skip
React = require("react")
Button = require("reactstrap").Button


def ButtonPanel(props):
    return __pragma__("xtrans", None, "{}", """ (
        <div className="flex-center">
            <div className='flex-container'>
                <Button
                    onClick={props.on_click_add}
                    color='success'
                >Add Todo</Button>
                <Button
                    onClick={props.clear_form_panel}
                    color='warning'
                >Clear Text</Button>
            </div>
        </div>
    ); """)
