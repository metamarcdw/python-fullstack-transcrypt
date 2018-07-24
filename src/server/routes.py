import uuid
import datetime

from flask import request
from flask_restplus import Resource, fields
from flask_jwt_extended import(
    create_access_token, get_jwt_identity, jwt_required
)
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from server import api, db, authorizations
from server.models import User, Todo


@api.route("/user")
class UsersResource(Resource):
    @jwt_required
    @api.marshal_list_with(User.user_shape, envelope="users")
    @api.doc(responses={
        401: "Not authenticated",
        403: "Not admin"
    })
    def get(self):
        User.abort_if_not_admin()
        # Get all users
        users = User.query.all()
        return users

    @api.expect(User.new_user_shape, validate=True)
    @api.marshal_with(User.user_shape, envelope="new_user")
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
    @api.marshal_with(User.user_shape, envelope="user")
    @api.doc(responses={
        401: "Not authenticated",
        403: "Not admin",
        404: "Not found"
    })
    def get(self, public_id):
        User.abort_if_not_admin()
        # Get one user
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            api.abort(404, "User not found")
        return user

    @jwt_required
    @api.marshal_with(User.user_shape, envelope="promoted_user")
    @api.doc(responses={
        400: "Already admin",
        401: "Not authenticated",
        403: "Not admin",
        404: "Not found"
    })
    def put(self, public_id):
        # Promote one user
        User.abort_if_not_admin()
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            api.abort(404, "User not found")
        if user.admin:
            api.abort(400, "User is already an admin")
        user.admin = True
        db.session.commit()
        return user

    @jwt_required
    @api.marshal_with(User.user_shape, envelope="deleted_user")
    @api.doc(responses={
        400: "Cannot delete self",
        401: "Not authenticated",
        403: "Not admin",
        404: "Not found"
    })
    def delete(self, public_id):
        # Delete one user
        current_user = get_jwt_identity()
        User.abort_if_not_admin(current_user=current_user)
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


@api.route("/todo")
class TodosResource(Resource):
    @jwt_required
    @api.marshal_list_with(Todo.todo_shape, envelope="todos")
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
    @api.expect(Todo.new_todo_shape, validate=True)
    @api.marshal_with(Todo.todo_shape, envelope="new_todo")
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
    @api.marshal_with(Todo.todo_shape, envelope="todo")
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
    @api.marshal_with(Todo.todo_shape, envelope="completed_todo")
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
    @api.marshal_with(Todo.todo_shape, envelope="deleted_todo")
    @api.doc(responses={
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
