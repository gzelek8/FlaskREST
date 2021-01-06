from datetime import datetime

from sqlalchemy.orm import validates

from flaskrest import db


class UnityError(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))
    # code_file = db.Column(db.String(20), default='default.cs')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @property
    def serialize(self):
        return {
            'line': self.line,
            'name': self.name,
            'description': self.description,
            # 'code_file': self.code_file,
            'date_posted': self.date_posted,
            'id': self.id,
            'user_id': self.user_id,
        }

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise AssertionError('No name provided')
        if len(name) < 2 or len(name) > 50:
            raise AssertionError('Name must be between 2 and 50 characters')
        return name

    @validates('description')
    def validate_description(self, key, description):
        if len(description) > 250:
            raise AssertionError('Description must be below 250 characters')
        return description

    @validates('line')
    def validate_line(self, key, line):
        if not line:
            raise AssertionError('No line provided')
        if not isinstance(line, int):
            raise ValueError('Line must be integer')
        return line
