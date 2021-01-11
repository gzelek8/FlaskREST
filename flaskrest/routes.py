import logging
from functools import wraps

import jwt
from flask import request, jsonify

from flaskrest import app
from flaskrest.Controller.UnityErrorsController import UnityErrorsController
from flaskrest.Controller.UsersController import UsersController
from flaskrest.models.User import User

errorsController = UnityErrorsController()
usersController = UsersController()
logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def logging():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-token' in request.cookies:
            token = request.cookies['x-access-token']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if 'x-access-token' in request.cookies:
                token = request.cookies['x-access-token']

            if not token:
                return jsonify({'message': 'You do not have access to that page. Sorry!'})

            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
            if not current_user.is_admin(access_level):
                return jsonify({'message': 'You do not have access to that page. Sorry!'})
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@app.route('/')
@app.route('/errors')
def showErrors():
    logging()
    return errorsController.getAllErrors()


@app.route('/errors/<int:error_id>')
def showError(error_id):
    logging()
    return errorsController.getSingleError(error_id)


@app.route('/errors', methods=['GET', 'POST'])
@token_required
def newError(current_user):
    logging()
    return errorsController.createNewError(current_user)


@app.route("/errors/<int:error_id>", methods=['PUT', 'PATCH'])
@token_required
def editError(current_user, error_id):
    logging()
    return errorsController.editError(error_id)


@app.route('/errors/<int:error_id>', methods=['DELETE'])
@token_required
def deleteError(current_user, error_id):
    logging()
    return errorsController.deleteError(current_user, error_id)


@app.route('/users')
@requires_access_level(True)
def showUsers():
    logging()
    return usersController.getAllUsers()


@app.route('/users/<int:user_id>')
@requires_access_level(True)
def showUser(user_id):
    logging()
    return usersController.getSingleUser(user_id)


@app.route('/users', methods=['GET', 'POST'])
def register():
    logging()
    return usersController.signupUser()


@app.route('/login', methods=['GET', 'POST'])  # rest exception
def login():
    logging()
    return usersController.loginUser()
