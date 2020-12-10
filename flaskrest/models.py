from datetime import datetime
from flaskrest import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    unity_errors = db.relationship('UnityError', backref='author', lazy=True)


class UnityError(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))
    code_file = db.Column(db.String(20), default='default.cs')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @property
    def serialize(self):
        return {
            'line': self.line,
            'name': self.name,
            'description': self.description,
            'code_file': self.code_file,
            'date_posted': self.date_posted,
            'id': self.id,
        }
