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


@app.route('/errors', methods=['GET', 'POST'])
def newError():
    line = request.args.get('line', '')
    name = request.args.get('name', '')
    description = request.args.get('description', '')
    username = request.args.get('username', '')
    newError = UnityError(line=line, name=name, description=description,
                          date_posted=datetime.utcnow(), username=username)
    db.session.add(newError)
    db.session.commit()
    flash('Your post has been submitted.', 'success')
    return jsonify(UnityError=newError.serialize)


@app.route("/errors/<int:error_id>", methods=['GET', 'POST'])
def editError(error_id, line, name, description):
    updatedError = UnityError.query.get_or_404(error_id)
    if not line:
        updatedError.line = line
    if not name:
        updatedError.name = name
    if not description:
        updatedError.description = description
    db.session.add(updatedError)
    db.session.commit()
    flash('Updated a Error with id %s' % id)
    return jsonify(UnityError=updatedError.serialize)


@app.route('/errors/<int:error_id>', methods=['GET', 'POST'])
def deleteError(error_id):
    deletedError = UnityError.query.get_or_404(error_id)
    if deletedError.author != current_user:
        abort(403)
    db.session.delete(deletedError)
    db.session.commit()
    flash('Your error has been deleted!', 'success')
    return 'Removed Error with id %s' % id
