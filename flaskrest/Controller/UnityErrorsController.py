from datetime import datetime

from flask import jsonify, make_response, request, abort

from flaskrest import db
from flaskrest.models.UnityError import UnityError


class UnityErrorsController:

    @staticmethod
    def getAllErrors():
        errors = db.session.query(UnityError).all()
        return make_response(jsonify(errors=[x.serialize for x in errors]), 200)

    @staticmethod
    def getSingleError(error_id):
        error = UnityError.query.get_or_404(error_id)
        return make_response(jsonify(error=error.serialize), 200)

    @staticmethod
    def createNewError(current_user):
        arg_req = request.get_json()
        line = arg_req['line']
        name = arg_req['name']
        description = arg_req['description']
        newError = UnityError(line=line, name=name, description=description,
                              date_posted=datetime.utcnow(), user_id=current_user.id)
        try:
            db.session.add(newError)
            db.session.commit()
            return make_response(jsonify(UnityError=newError.serialize), 201)
        except AssertionError as exception_message:
            return make_response(jsonify(msg='Error: {}. '.format(exception_message)), 400)

    @staticmethod
    def editError(error_id):
        updatedError = request.get_json()
        updateError = UnityError.query.get_or_404(error_id)
        if 'line' in updatedError:
            updateError.line = updatedError['line']
        if 'name' in updatedError:
            updateError.name = updatedError['name']
        if 'description' in updatedError:
            updateError.description = updatedError['description']
        try:
            db.session.commit()
            return make_response(jsonify(UnityError=updateError.serialize), 200)
        except AssertionError as exception_message:
            return make_response(jsonify(msg='Error: {}. '.format(exception_message)), 400)

    @staticmethod
    def deleteError(current_user, error_id):
        deletedError = UnityError.query.get_or_404(error_id)
        if deletedError.author != current_user:
            abort(403)
        db.session.delete(deletedError)
        db.session.commit()
        print('Your error has been deleted!', 'success')

        return make_response(jsonify({'result': True}), 204)
