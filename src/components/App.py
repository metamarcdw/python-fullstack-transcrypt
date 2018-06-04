from Component_py.stubs import require, __pragma__, console  # __:skip
from Component_py.component import Component, destruct
from containers.LoginFormContainer import LoginFormContainer
from containers.FormPanelContainer import FormPanelContainer
from containers.ButtonPanelContainer import ButtonPanelContainer
from components.TodoList import TodoList

React = require("react")
Row, Col, Jumbotron = destruct(
    require("reactstrap"), "Row", "Col", "Jumbotron")


class App(Component):
    def __init__(self, props):
        super().__init__(props)
        self.state = {
            "todos": [
                {
                    "id": 1,
                    "text": "Balls"
                },
                {
                    "id": 2,
                    "text": "Royce"
                }
            ]
        }

    def on_click_login(self, e):
        e.preventDefault()
        username, password = destruct(
            self.props["login_form"], "username_text", "password_text")
        if username and password:
            self.props.do_login(username, password)

    def on_click_add(self):
        console.log("ADD")

    def render(self):
        def render_login_panel():
            return __pragma__("xtrans", None, "{}", """ (
                <div>
                    <h5>Please Login:</h5>
                    <LoginFormContainer on_click={self.on_click_login} />
                </div>
            ); """)

        def render_todo_panel():
            return __pragma__("xtrans", None, "{}", """ (
                <div>
                    <TodoList todos={self.state.todos} />
                    <FormPanelContainer />
                    <ButtonPanelContainer on_click_add={self.on_click_add} />
                </div>
            ); """)

        login = self.props["login_user"]
        visible_component = render_todo_panel() if login["logged_in"] else render_login_panel()

        return __pragma__("xtrans", None, "{}", """ (
            <Row>
                <Col
                    lg={{size: 6, offset: 3}}
                    md={{size: 8, offset: 2}}
                    sm={{size: 10, offset: 1}}
                >
                    <Jumbotron>
                        <div className="flex-column">
                            <div className="flex-center padding">
                                <h2>My Todos</h2>
                            </div>
                            {visible_component}
                            <span className="red-text">{login.error}</span>
                        </div>
                    </Jumbotron>
                </Col>
            </Row>
        ); """)
