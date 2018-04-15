import datetime
import uuid
from flask import Flask, request
from flask_restplus import Api, Resource, fields
from flask_jwt_extended import(
    JWTManager, create_access_token, get_jwt_identity, jwt_required
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)

FILE_PATH = r"C:\Users\cypher\Desktop\fullstack-react\react-native\todos_fs\server"
app.config["JWT_SECRET_KEY"] = "asecret"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{FILE_PATH}\\db.sqlite3"

jwt = JWTManager(app)
jwt._set_error_handler_callbacks(api)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    admin = db.Column(db.Boolean)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50), nullable=False)
    complete = db.Column(db.Boolean)
    user = db.Column(db.Integer,
                     db.ForeignKey('user.id'),
                     nullable=False)

@api.route("/user", "/user/<string:public_id>")
class UserResource(Resource):
    user_shape = api.model("user_shape", {
        "id": fields.String(attribute="public_id"),
        "name": fields.String,
        "password_hash": fields.String,
        "admin": fields.Boolean
    })
    new_user_shape = api.model("new_user_shape", {
        "name": fields.String,
        "password": fields.String
    })

    def _abort_if_not_admin(self):
        current_user = get_jwt_identity()
        if not current_user["admin"]:
            api.abort(403, "Must be admin")

    @jwt_required
    @api.marshal_with(user_shape, envelope="users")
    def get(self, public_id=None):
        self._abort_if_not_admin()
        if public_id:
            # Get one user
            user = User.query.filter_by(public_id=public_id).first()
            if not user:
                api.abort(404, "User not found")
            return user
        else:
            # Get all users
            users = User.query.all()
            if not users:
                api.abort(404, "No users found")
            return users

    @jwt_required
    @api.expect(new_user_shape)
    @api.marshal_with(user_shape, envelope="new_user")
    def post(self, public_id=None):
        # Create one user
        self._abort_if_not_admin()
        data = api.payload
        if not data or not "name" in data or not "password" in data:
            api.abort(401, "Malformed request")
        new_user = User(public_id=str(uuid.uuid4()),
                        name=data["name"],
                        password_hash=generate_password_hash(data["password"]),
                        admin=False)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @jwt_required
    @api.marshal_with(user_shape, envelope="promoted_user")
    def put(self, public_id=None):
        # Promote one user
        self._abort_if_not_admin()
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            api.abort(404, "User not found")
        user.admin = True
        db.session.commit()
        return user

    @jwt_required
    def delete(self, public_id=None):
        # Delete one user
        self._abort_if_not_admin()
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            api.abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully."}

@api.route("/login")
class LoginResource(Resource):
    def get(self):
        auth = request.authorization
        if not auth or not auth["username"] or not auth["password"]:
            api.abort(401, "Login attempt failed")
        user = User.query.filter_by(name=auth["username"]).first()
        if not user:
            api.abort(401, "Login attempt failed")
        if not check_password_hash(user.password_hash, auth["password"]):
            api.abort(401, "Login attempt failed")
        identity = {"name": user.name, "admin": user.admin}
        expiry = datetime.timedelta(minutes=30)
        return {"token": create_access_token(identity, expires_delta=expiry)}

@api.route("/todo", "/todo/<int:id>")
class TodoResource(Resource):
    todo_shape = api.model("todo_shape", {
        "id": fields.Integer,
        "text": fields.String,
        "complete": fields.Boolean
    })
    new_todo_shape = api.model("new_todo_shape", {
        "text": fields.String
    })

    @jwt_required
    @api.marshal_with(todo_shape, envelope="todos")
    def get(self, id=None):
        current_user = get_jwt_identity()
        user = User.query.filter_by(name=current_user["name"]).first()
        if id:
            # Get one todo
            todo = Todo.query.filter_by(id=id, user=user.id).first()
            if not todo:
                api.abort(404, "Todo not found")
            return todo
        else:
            # Get all todos for this user
            todos = Todo.query.filter_by(user=user.id).all()
            if not todos:
                api.abort(404, "No todos found")
            return todos

    @jwt_required
    @api.expect(new_todo_shape)
    @api.marshal_with(todo_shape, envelope="new_todo")
    def post(self, id=None):
        # Create a new todo
        current_user = get_jwt_identity()
        user = User.query.filter_by(name=current_user["name"]).first()
        data = api.payload
        if not data or not "text" in data:
            api.abort(401, "Malformed request")
        new_todo = Todo(text=data["text"],
                        complete=False,
                        user=user.id)
        db.session.add(new_todo)
        db.session.commit()
        return new_todo

    @jwt_required
    @api.marshal_with(todo_shape, envelope="completed_todo")
    def put(self, id=None):
        # Complete a todo
        current_user = get_jwt_identity()
        user = User.query.filter_by(name=current_user["name"]).first()
        todo = Todo.query.filter_by(id=id, user=user.id).first()
        if not todo:
            api.abort(404, "Todo not found")
        todo.complete = True
        db.session.commit()
        return todo

    @jwt_required
    def delete(self, id=None):
        # Delete a todo
        current_user = get_jwt_identity()
        user = User.query.filter_by(name=current_user["name"]).first()
        todo = Todo.query.filter_by(id=id, user=user.id).first()
        if not todo:
            api.abort(404, "Todo not found")
        db.session.delete(todo)
        db.session.commit()
        return {"message": "Todo deleted successfully."}

if __name__ == "__main__":
    app.run(debug=True)
