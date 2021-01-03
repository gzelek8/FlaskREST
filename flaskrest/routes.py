from datetime import datetime

from flask import flash, abort, jsonify, request
from flask_login import current_user

from flaskrest import app, db
from flaskrest.models import UnityError


@app.route('/')
@app.route('/errors')
def showErrors():
    errors = db.session.query(UnityError).all()
    return jsonify(errors=[x.serialize for x in errors])


@app.route('/errors/<int:error_id>')
def showError(error_id):
    errors = UnityError.query.get_or_404(error_id)
    return jsonify(errors=errors.serialize)


@app.route('/errors', methods=['POST'])
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
    return jsonify(UnityError=newError.serialize)


@app.route("/errors/<int:error_id>", methods=['PUT'])
def editError(error_id):
    updatedError = UnityError.query.get_or_404(error_id)
    if 'line' in request.form:
        updatedError.line = request.form['line']
    if 'name' in request.form:
        updatedError.name = request.form.get('name', '')
    if 'description' in request.form:
        updatedError.description = request.form.get('description', '')
    db.session.commit()
    print('Updated a Error with id %s' % id)
    return jsonify(UnityError=updatedError.serialize)


@app.route('/errors/<int:error_id>', methods=['DELETE'])
def deleteError(error_id):
    deletedError = UnityError.query.get_or_404(error_id)
    # if deletedError.author != current_user:
    #     abort(403)
    db.session.delete(deletedError)
    db.session.commit()
    print('Your error has been deleted!', 'success')
    return jsonify({'result': True})


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
