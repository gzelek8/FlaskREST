from datetime import datetime

from flask_login import UserMixin

from flaskrest import db


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     unity_errors = db.relationship('UnityError', backref='author', lazy=True)
#     about_me = db.Column(db.String(140))
#     last_seen = db.Column(db.DateTime, default=datetime.utcnow)
#
#     @property
#     def serialize(self):
#         return {
#             'username': self.username,
#             'password': self.password,
#             'email': self.email,
#             'about_me': self.about_me,
#             'id': self.id,
#             'last_seen': self.last_seen,
#             'unity_errors': self.unity_errors,
#         }


class UnityError(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))
    # code_file = db.Column(db.String(20), default='default.cs')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)

    @property
    def serialize(self):
        return {
            'line': self.line,
            'name': self.name,
            'description': self.description,
            # 'code_file': self.code_file,
            'date_posted': self.date_posted,
            'username': self.username,
            'id': self.id,
        }
