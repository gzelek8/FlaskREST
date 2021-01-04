from datetime import datetime

from flask import flash, abort, jsonify, request, make_response
from flask_login import current_user

from flaskrest import app, db
from flaskrest.models import UnityError


@app.route('/')
@app.route('/errors')
def showErrors():
    errors = db.session.query(UnityError).all()
    return make_response(jsonify(errors=[x.serialize for x in errors]), 200)


@app.route('/errors/<int:error_id>')
def showError(error_id):
    errors = UnityError.query.get_or_404(error_id)
    return make_response(jsonify(errors=errors.serialize), 200)


@app.route('/errors', methods=['GET', 'POST'])
def newError():
    line = request.form['line']
    name = request.form['name']
    description = request.form['description']
    username = request.form['username']
    newError = UnityError(line=line, name=name, description=description,
                          date_posted=datetime.utcnow(), username=username)
    db.session.add(newError)
    db.session.commit()
    print('Your post has been submitted.', 'success')

    return make_response(jsonify(UnityError=newError.serialize), 201)


@app.route("/errors/<int:error_id>", methods=['PUT', 'PATCH'])
def editError(error_id):
    updatedError = request.get_json()
    updateError = UnityError.query.get_or_404(error_id)
    if 'line' in updatedError:
        updateError.line = updatedError['line']
    if 'name' in updatedError:
        updateError.name = updatedError['name']
    if 'description' in updatedError:
        updateError.description = updatedError['description']
    db.session.commit()
    return make_response(jsonify(UnityError=updateError.serialize), 200)


@app.route('/errors/<int:error_id>', methods=['DELETE'])
def deleteError(error_id):
    deletedError = UnityError.query.get_or_404(error_id)
    # if deletedError.author != current_user:
    #     abort(403)
    db.session.delete(deletedError)
    db.session.commit()
    print('Your error has been deleted!', 'success')

    return make_response(jsonify({'result': True}), 204)

# @app.route('/users')
# def showUsers():
#     users = db.session.query(User).all()
#     return jsonify(errors=[x.serialize for x in users])
#
#
# @app.route("/register", methods=['POST'])
# def register():
#     username = request.form['username']
#     email = request.form['email']
#     password = request.form['password']
#     about_me = request.form['about_me']
#     user = User(username=username, email=email, password=password, about_me=about_me)
#     db.session.add(user)
#     db.session.commit()
#     print('Your acount has been created.', 'success')
#     return jsonify(User=user.serialize)
