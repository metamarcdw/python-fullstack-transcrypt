from server import db
from server.mixins import UserMixin, TodoMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    todos = db.relationship("Todo", backref="user", cascade="all,delete")

    def __repr__(self):
        return f"<User name: {self.name}, admin: {self.admin}>"


class Todo(db.Model, TodoMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(30), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)

    def __repr__(self):
        return f"<Todo text: {self.text}, complete: {self.complete}>"
