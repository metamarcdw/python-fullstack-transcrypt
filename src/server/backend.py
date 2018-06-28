import os
import datetime
import uuid
from flask import Flask, request
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
from flask_jwt_extended import(
    JWTManager, create_access_token, get_jwt_identity, jwt_required
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

authorizations = {
    "bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    },
    "basic": {
        "type": "basic"
    }
}

cors_resources = {
    r"/*": {
        "origins": [
            "https://metamarcdw.github.io",
            "http://localhost:3000"
        ],
        "supports_credentials": True
    }
}

api = Api(authorizations=authorizations)
cors = CORS(resources=cors_resources)

db = SQLAlchemy()
jwt = JWTManager()
jwt._set_error_handler_callbacks(api)
# https://github.com/vimalloc/flask-jwt-extended/issues/83


def create_app():
    mode = os.environ.get("TODOS_FS_MODE")
    config_type = None

    # Specifying the 'server' module is needed when run indirectly
    if mode == "production":
        config_type = "server.config.ProductionConfig"
    elif mode == "development":
        config_type = "config.DevelopmentConfig"
    elif mode == "testing":
        config_type = "server.config.TestingConfig"
    else:
        raise ValueError("Mode variable not set.")
    print(f" * Running the API in {mode} mode.")

    app = Flask(__name__)
    app.config.from_object(config_type)

    api.init_app(app)
    cors.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    return app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    todos = db.relationship("Todo", backref="user", cascade="all,delete")


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(30), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)


class UserUtil:
    user_shape = api.model("user_shape", {
        "id": fields.String(
            description="This user's public ID",
            example="1226637d-6d9a-4d5b-a7c6-9b1d5bba98f8",
            attribute="public_id",
            required=True),
        "name": fields.String(
            description="This user's name",
            example="metamarcdw",
            required=True),
        "password_hash": fields.String(
            description="This user's hashed password",
            example="pbkdf2:sha256:50000$Dm5rUTw7$...",
            required=True),
        "admin": fields.Boolean(
            description="This user's admin status",
            example="false",
            required=True)
    })
    new_user_shape = api.model("new_user_shape", {
        "name": fields.String(
            min_length=1, max_length=30, required=True),
        "password": fields.String(
            min_length=1, required=True)
    })

    @staticmethod
    def abort_if_not_admin(current_user=None):
        if not current_user:
            current_user = get_jwt_identity()
        if not current_user["admin"]:
            api.abort(403, "Must be admin")


@api.route("/user")
class UsersResource(Resource):
    @jwt_required
    @api.marshal_list_with(UserUtil.user_shape, envelope="users")
    @api.doc(responses={
        401: "Not authenticated",
        403: "Not admin"
    })
    def get(self):
        UserUtil.abort_if_not_admin()
        # Get all users
        users = User.query.all()
        return users

    @api.expect(UserUtil.new_user_shape, validate=True)
    @api.marshal_with(UserUtil.user_shape, envelope="new_user")
    @api.doc(responses={
        400: "Malformed request OR User exists"
    })
    def post(self):
        # Create one user
        name, password = api.payload["name"], api.payload["password"]
        try:
            new_user = User(public_id=str(uuid.uuid4()),
                            name=name,
                            password_hash=generate_password_hash(password),
                            admin=False)
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            api.abort(400, "A user with this name already exists")
        return new_user


@api.route("/user/<string:public_id>")
class UserResource(Resource):
    @jwt_required
    @api.marshal_with(UserUtil.user_shape, envelope="users")
    @api.doc(responses={
        401: "Not authenticated",
        403: "Not admin",
        404: "Not found"
    })
    def get(self, public_id):
        UserUtil.abort_if_not_admin()
        # Get one user
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            api.abort(404, "User not found")
        return user

    @jwt_required
    @api.marshal_with(UserUtil.user_shape, envelope="promoted_user")
    @api.doc(responses={
        400: "Already admin",
        401: "Not authenticated",
        403: "Not admin",
        404: "Not found"
    })
    def put(self, public_id):
        # Promote one user
        UserUtil.abort_if_not_admin()
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            api.abort(404, "User not found")
        if user.admin:
            api.abort(400, "User is already an admin")
        user.admin = True
        db.session.commit()
        return user

    @jwt_required
    @api.marshal_with(UserUtil.user_shape, envelope="deleted_user")
    @api.doc(responses={
        200: "Success",
        400: "Cannot delete self",
        401: "Not authenticated",
        403: "Not admin",
        404: "Not found"
    })
    def delete(self, public_id):
        # Delete one user
        current_user = get_jwt_identity()
        UserUtil.abort_if_not_admin(current_user=current_user)
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            api.abort(404, "User not found")
        if user.name == current_user["name"]:
            api.abort(400, "Cannot delete your own user")
        db.session.delete(user)
        db.session.commit()
        return user


@api.route("/login")
class LoginResource(Resource):
    token_shape = api.model("token_shape", {
        "token": fields.String(
            description="A JWT associated with the current user's session",
            example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            required=True)
    })

    @api.marshal_with(token_shape)
    @api.doc(security={"basic": authorizations["basic"]},
             responses={401: "Login failed"})
    def get(self):
        auth = request.authorization
        if not auth or not all(k in auth for k in ("username", "password")):
            api.abort(401, "Login attempt failed")

        name, password = auth["username"], auth["password"]
        user = User.query.filter_by(name=name).first()
        if not user or not check_password_hash(user.password_hash, password):
            api.abort(401, "Login attempt failed")

        identity = {"name": user.name, "admin": user.admin}
        expiry = datetime.timedelta(minutes=30)
        return {"token": create_access_token(identity, expires_delta=expiry)}


class TodoUtil:
    todo_shape = api.model("todo_shape", {
        "id": fields.Integer(
            description="A unique identifier for todos",
            example="5",
            required=True),
        "text": fields.String(
            description="Some text describing your task",
            example="Do a thing.",
            required=True),
        "complete": fields.Boolean(
            description="This todo's completion status",
            example="true",
            required=True)
    })
    new_todo_shape = api.model("new_todo_shape", {
        "text": fields.String(
            min_length=1, max_length=30, required=True)
    })


@api.route("/todo")
class TodosResource(Resource):
    @jwt_required
    @api.marshal_list_with(TodoUtil.todo_shape, envelope="todos")
    @api.doc(responses={
        401: "Not authenticated",
        404: "Not found"
    })
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(name=current_user["name"]).first()
        # Get all todos for this user
        if not user.todos:
            api.abort(404, "No todos found")
        return user.todos

    @jwt_required
    @api.expect(TodoUtil.new_todo_shape, validate=True)
    @api.marshal_with(TodoUtil.todo_shape, envelope="new_todo")
    @api.doc(responses={
        400: "Malformed request",
        401: "Not authenticated"
    })
    def post(self):
        # Create a new todo
        current_user = get_jwt_identity()
        user = User.query.filter_by(name=current_user["name"]).first()
        text = api.payload["text"]
        new_todo = Todo(text=text,
                        complete=False,
                        user=user)
        db.session.add(new_todo)
        db.session.commit()
        return new_todo


@api.route("/todo/<int:id>")
class TodoResource(Resource):
    @jwt_required
    @api.marshal_with(TodoUtil.todo_shape, envelope="todos")
    @api.doc(responses={
        401: "Not authenticated",
        404: "Not found"
    })
    def get(self, id):
        current_user = get_jwt_identity()
        user = User.query.filter_by(name=current_user["name"]).first()
        # Get one todo
        todo = Todo.query.filter_by(id=id, user=user).first()
        if not todo:
            api.abort(404, "Todo not found")
        return todo

    @jwt_required
    @api.marshal_with(TodoUtil.todo_shape, envelope="completed_todo")
    @api.doc(responses={
        401: "Not authenticated",
        404: "Not found"
    })
    def put(self, id):
        # Complete a todo
        current_user = get_jwt_identity()
        user = User.query.filter_by(name=current_user["name"]).first()
        todo = Todo.query.filter_by(id=id, user=user).first()
        if not todo:
            api.abort(404, "Todo not found")
        todo.complete = True
        db.session.commit()
        return todo

    @jwt_required
    @api.marshal_with(TodoUtil.todo_shape, envelope="deleted_todo")
    @api.doc(responses={
        200: "Success",
        401: "Not authenticated",
        404: "Not found"
    })
    def delete(self, id):
        # Delete a todo
        current_user = get_jwt_identity()
        user = User.query.filter_by(name=current_user["name"]).first()
        todo = Todo.query.filter_by(id=id, user=user).first()
        if not todo:
            api.abort(404, "Todo not found")
        db.session.delete(todo)
        db.session.commit()
        return todo


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run()
