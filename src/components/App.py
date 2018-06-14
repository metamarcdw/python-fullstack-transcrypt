from Component_py.stubs import require, __pragma__  # __:skip
from Component_py.component import destruct
from containers.LoginFormContainer import LoginFormContainer
from containers.FormPanelContainer import FormPanelContainer
from containers.ButtonPanelContainer import ButtonPanelContainer
from containers.TodoListContainer import TodoListContainer

React = require("react")
Row, Col, Jumbotron = destruct(
    require("reactstrap"), "Row", "Col", "Jumbotron")


def App(props):
    def render_login_panel():
        return __pragma__("xtrans", None, "{}", """ (
            <div>
                <h5>Please Login:</h5>
                <LoginFormContainer />
            </div>
        ); """)

    def render_todo_panel():
        return __pragma__("xtrans", None, "{}", """ (
            <div>
                <TodoListContainer />
                <FormPanelContainer />
                <ButtonPanelContainer />
            </div>
        ); """)

    logged_in, error = destruct(props["login_user"], "logged_in", "error")
    visible_component = render_todo_panel() if logged_in else render_login_panel()

    return __pragma__("xtrans", None, "{}", """ (
        <Row>
            <Col
                lg={{size: 6, offset: 3}}
                md={{size: 8, offset: 2}}
                sm={{size: 10, offset: 1}}
                xs="12"
            >
                <Jumbotron>
                    <div className="flex-column">
                        <div className="flex-center padding">
                            <h2>My Todos</h2>
                        </div>
                        {visible_component}
                        <span className="red-text">{error}</span>
                    </div>
                </Jumbotron>
            </Col>
        </Row>
    ); """)
