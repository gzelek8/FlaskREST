import datetime
import uuid

import jwt
from flask import request, jsonify, make_response
from werkzeug.security import (generate_password_hash, check_password_hash)

from flaskrest import db, app
from flaskrest.models.User import User


class UsersController:

    @staticmethod
    def signup_user():
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data['email']
        hashed_password = generate_password_hash(password, method='sha256')

        newUser = User(public_id=str(uuid.uuid4()), username=username, password=hashed_password, email=email,
                       admin=False)
        try:
            db.session.add(newUser)
            db.session.commit()
            return make_response(jsonify(User=newUser.serialize), 201)
        except AssertionError as exception_message:
            return make_response(jsonify(msg='Error: {}. '.format(exception_message)), 400)

    @staticmethod
    def login_user():

        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        user = User.query.filter_by(username=auth.username).first()

        if check_password_hash(user.password, auth.password):
            token = jwt.encode(
                {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                app.config['SECRET_KEY'])
            return jsonify({'token': token.decode('UTF-8')})

        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    @staticmethod
    def get_all_users():
        users = db.session.query(User).all()
        return make_response(jsonify(users=[x.serialize for x in users]), 200)
