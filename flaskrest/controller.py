from flaskrest import db
from flask import jsonify, make_response, request
from flaskrest.models import UnityError
from datetime import datetime


class Controller:

    def getAllErrors(self):
        errors = db.session.query(UnityError).all()
        return make_response(jsonify(errors=[x.serialize for x in errors]), 200)

    @staticmethod
    def getSingleError(error_id):
        errors = UnityError.query.get_or_404(error_id)
        return make_response(jsonify(errors=errors.serialize), 200)

    @staticmethod
    def createNewError():
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

    def editError(self, error_id):
        #updatedError = request.get_json()
        updateError = UnityError.query.get_or_404(error_id)
        if 'line' in request.form:
            updateError.line = request.form['line']
        if 'name' in request.form:
            updateError.name = request.form['name']
        if 'description' in request.form:
            updateError.description = request.form['description']
        db.session.commit()
        return make_response(jsonify(UnityError=updateError.serialize), 200)

    def deleteError(self, error_id):
        deletedError = UnityError.query.get_or_404(error_id)
        # if deletedError.author != current_user:
        #     abort(403)
        db.session.delete(deletedError)
        db.session.commit()
        print('Your error has been deleted!', 'success')

        return make_response(jsonify({'result': True}), 204)