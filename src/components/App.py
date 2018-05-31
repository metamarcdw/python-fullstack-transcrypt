from Component_py.stubs import require, __pragma__  # __:skip
from Component_py.component import Component, destruct
from containers.LoginFormContainer import LoginFormContainer
from containers.FormPanelContainer import FormPanelContainer
from components.TodoList import TodoList
from components.ButtonPanel import ButtonPanel
from store import store

React = require("react")
Row, Col, Jumbotron = destruct(
    require("reactstrap"), "Row", "Col", "Jumbotron")
Provider = require("react-redux").Provider


class App(Component):
    def __init__(self, props):
        super().__init__(props)
        self.state = {
            "logged_in": True,
            "todos": [
                {
                    "id": 1,
                    "text": "text"
                },
                {
                    "id": 2,
                    "text": "tiddies"
                }
            ]
        }

    def on_login(self, e):
        e.preventDefault()

    def render(self):
        def render_login_panel():
            return __pragma__("xtrans", None, "{}", """ (
                <div>
                    <h5>Please Login:</h5>
                    <LoginFormContainer
                        on_click={self.on_login} />
                </div>
            ); """)

        def render_todo_panel():
            return __pragma__("xtrans", None, "{}", """ (
                <div>
                    <TodoList todos={self.state.todos} />
                    <FormPanelContainer />
                    <ButtonPanel />
                </div>
            ); """)

        component = render_todo_panel() if self.state["logged_in"] \
            else render_login_panel()
        return __pragma__("xtrans", None, "{}", """ (
            <Provider store={store}>
                <Row>
                    <Col lg={{size: 6, offset: 3}} md={{size: 8, offset: 2}} sm={{size: 10, offset: 1}}>
                        <Jumbotron>
                            <div className="flex-column">
                                <div className="flex-center padding">
                                    <h2>My Todos</h2>
                                </div>
                                {component}
                            </div>
                        </Jumbotron>
                    </Col>
                </Row>
            </Provider>
        ); """)
