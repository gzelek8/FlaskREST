import re

from sqlalchemy.orm import validates

from flaskrest import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    username = db.Column(db.String(20), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128))
    admin = db.Column(db.Boolean)
    unity_errors = db.relationship('UnityError', backref='author', lazy=True)

    # about_me = db.Column(db.String(140))
    # last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def serialize(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            # 'about_me': self.about_me,
            'id': self.id,
            'public_id': self.public_id,
            # 'last_seen': self.last_seen,
            'unity_errors': [x.serialize for x in self.unity_errors],
            'admin': self.admin,
        }

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise AssertionError('No username provided')
        if User.query.filter(User.username == username).first():
            raise AssertionError('Username is already in use')
        if len(username) < 3 or len(username) > 20:
            raise AssertionError('Username must be between 3 and 20 characters')
        return username

    @validates('email')
    def validate_email(self, key, email):
        if not email:            raise AssertionError('No email provided')
        if User.query.filter(User.email == email).first():
            raise AssertionError('Email is already in use')
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError('Provided email is not an email address')
        return email
