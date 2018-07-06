
from flask_restplus import fields
from flask_jwt_extended import get_jwt_identity
from server import api


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
