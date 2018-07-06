import os
import uuid
import base64

import pytest
from flask import url_for
from werkzeug.security import generate_password_hash

from server import create_app, db as _db
from server.models import User, Todo


@pytest.fixture(scope="session")
def app():
    os.environ["TODOS_FS_MODE"] = "testing"
    flask_app = create_app()
    return flask_app


#pylint: disable=W0621
@pytest.fixture(scope="session", autouse=True)
def db(app):
    def create_user(username, password, admin=False):
        return User(public_id=str(uuid.uuid4()),
                    name=username,
                    password_hash=generate_password_hash(password),
                    admin=admin)

    def create_todo(text, user, complete=False):
        return Todo(text=text,
                    complete=complete,
                    user=user)

    if os.path.exists(app.config['DB_PATH']):
        os.unlink(app.config['DB_PATH'])

    with app.app_context():
        _db.init_app(app)
        _db.create_all()

        admin_user = create_user("Admin", "password", admin=True)
        regular_user = create_user("User", "snowman")
        promotable_user = create_user("Promotable User", "greenman")
        _db.session.add(admin_user)
        _db.session.add(regular_user)
        _db.session.add(promotable_user)

        incomplete_todo = create_todo("Incomplete", regular_user)
        complete_todo = create_todo("Complete", regular_user, complete=True)
        _db.session.add(incomplete_todo)
        _db.session.add(complete_todo)

        _db.session.commit()
        yield _db
        _db.drop_all()


@pytest.fixture
def user_public_id():
    user = User.query.filter_by(name="Promotable User").first()
    return user.public_id


def get_token(client, username, password):
    bytes_ = f"{username}:{password}".encode("utf-8")
    auth = base64.b64encode(bytes_).decode("ascii")
    token_response = client.get(url_for("login_resource"), headers={
        "Authorization": f"Basic {auth}"
    })
    return token_response.json["token"]


@pytest.fixture
def admin_token(client):
    return get_token(client, "Admin", "password")


@pytest.fixture
def user_token(client):
    return get_token(client, "User", "snowman")
