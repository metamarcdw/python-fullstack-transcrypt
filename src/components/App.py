from Component_py.stubs import require, __pragma__  # __:skip
from Component_py.component import Component, destruct

from containers.LoginFormContainer import LoginFormContainer
from containers.FormPanelContainer import FormPanelContainer
from containers.ButtonPanelContainer import ButtonPanelContainer
from containers.TodoListContainer import TodoListContainer
from components.Spinner import Spinner

React = require("react")
PropTypes = require("prop-types")
Form, Row, Col, Jumbotron = destruct(
    require("reactstrap"), "Form", "Row", "Col", "Jumbotron")


class App(Component):
    propTypes = {
        "logged_in": PropTypes.bool.isRequired,
        "error": PropTypes.string
    }

    def render_login_panel(self):
        return __pragma__("xtrans", None, "{}", """ (
            <div>
                <h5>Please Login:</h5>
                <LoginFormContainer />
            </div>
        ); """)

    def on_submit(self, e):
        e.preventDefault()

    def render_todo_panel(self):
        return __pragma__("xtrans", None, "{}", """ (
            <div>
                <TodoListContainer />
                <Form
                    className="p-4"
                    onSubmit={self.on_submit}
                >
                    <FormPanelContainer />
                    <ButtonPanelContainer />
                </Form>
            </div>
        ); """)

    def render(self):
        logged_in, loading, error = destruct(
            self.props, "logged_in", "loading", "error")
        visible_component = \
            self.render_todo_panel() if logged_in else self.render_login_panel()

        return __pragma__("xtrans", None, "{}", """ (
            <Row>
                <Col
                    lg={{size: 6, offset: 3}}
                    md={{size: 8, offset: 2}}
                    sm={{size: 10, offset: 1}}
                    xs="12"
                >
                    <Jumbotron>
                        <div className="d-flex flex-column">
                            <div className="d-flex justify-content-center align-items-center p-4">
                                <h2>My Todos</h2>
                            </div>
                            {visible_component}
                            <Spinner loading={loading} />
                            <span className="text-danger">{error}</span>
                        </div>
                    </Jumbotron>
                </Col>
            </Row>
        ); """)
