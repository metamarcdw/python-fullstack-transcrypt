import os
import uuid
import base64

import pytest
from flask import url_for
from werkzeug.security import generate_password_hash

from server.backend import create_app, User, db as _db


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

    if os.path.exists(app.config['DB_PATH']):
        os.unlink(app.config['DB_PATH'])

    with app.app_context():
        _db.init_app(app)
        _db.create_all()

        _db.session.add(create_user("Jesus", "password", admin=True))
        _db.session.add(create_user("Cocaine", "snowman"))
        _db.session.commit()

        yield _db
        _db.drop_all()


def get_token(client, username, password):
    bytes_ = f"{username}:{password}".encode("utf-8")
    auth = base64.b64encode(bytes_).decode("ascii")
    token_response = client.get(url_for("login_resource"), headers={
        "Authorization": f"Basic {auth}"
    })
    return token_response.json["token"]


@pytest.fixture
def admin_token(client):
    return get_token(client, "Jesus", "password")


@pytest.fixture
def user_token(client):
    return get_token(client, "Cocaine", "snowman")
