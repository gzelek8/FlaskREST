from flaskrest import app
from flaskrest.controller import Controller

controller = Controller()


@app.route('/')
@app.route('/errors')
def showErrors():
    return controller.getAllErrors()


@app.route('/errors/<int:error_id>')
def showError(error_id):
    return controller.getSingleError(error_id)


@app.route('/errors', methods=['GET', 'POST'])
def newError():
    return controller.createNewError()


@app.route("/errors/<int:error_id>", methods=['PUT', 'PATCH'])
def editError(error_id):
    return controller.editError(error_id)


@app.route('/errors/<int:error_id>', methods=['DELETE'])
def deleteError(error_id):
    return controller.deleteError(error_id)


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
