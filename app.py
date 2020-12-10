from flask import Flask, render_template, request, redirect, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'c6eef9e5b42780f9bb355cc25a85da78'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, UnityError

# Connect to Database and create database session
engine = create_engine('sqlite:///unity-errors.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('showErrors'))
    return render_template('register.html', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/')
@app.route('/errors')
def showErrors():
    errors = session.query(UnityError).all()
    return render_template('home.html', errors=errors)


@app.route('/errors/new/', methods=['GET', 'POST'])
def newError():
    if request.method == 'POST':
        newError = UnityError(line=request.form['line'],
                              name=request.form['name'],
                              description=request.form['description'])
        session.add(newError)
        session.commit()
        return redirect(url_for('showErrors'))
    else:
        return render_template('newError.html')


@app.route("/errors/<int:error_id>/edit/", methods=['GET', 'POST'])
def editError(error_id):
    editedError = session.query(UnityError).filter_by(id=error_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedError.description = request.form['name']
            return redirect(url_for('showErrors'))
    else:
        return render_template('editError.html', error=editedError)


@app.route('/errors/<int:error_id>/delete/', methods=['GET', 'POST'])
def deleteError(error_id):
    errorToDelete = session.query(UnityError).filter_by(id=error_id).one()
    if request.method == 'POST':
        session.delete(errorToDelete)
        session.commit()
        return redirect(url_for('showErrors', error_id=error_id))
    else:
        return render_template('deleteError.html', error=errorToDelete)


"""
api functions
"""
from flask import jsonify


def get_errors():
    errors = session.query(UnityError).all()
    return jsonify(errors=[x.serialize for x in errors])


def get_error(error_id):
    errors = session.query(UnityError).filter_by(id=error_id).one()
    return jsonify(errors=errors.serialize)


def makeANewError(line, name, description):
    addederror = UnityError(line=line, name=name, description=description)
    session.add(addederror)
    session.commit()
    return jsonify(UnityError=addederror.serialize)


def updateError(id, line, name, description):
    updatedError = session.query(UnityError).filter_by(id=id).one()
    if not line:
        updatedError.line = line
    if not name:
        updatedError.name = name
    if not description:
        updatedError.description = description
    session.add(updatedError)
    session.commit()
    return 'Updated a Error with id %s' % id


def deleteAnError(id):
    errorToDelete = session.query(UnityError).filter_by(id=id).one()
    session.delete(errorToDelete)
    session.commit()
    return 'Removed Error with id %s' % id


@app.route('/errorsApi', methods=['GET', 'POST'])
def errorsFunction():
    if request.method == 'GET':
        return get_errors()
    elif request.method == 'POST':
        line = request.args.get('line', '')
        name = request.args.get('name', '')
        description = request.args.get('description', '')
        return makeANewError(line, name, description)


@app.route('/errorsApi/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def errorFunctionId(id):
    if request.method == 'GET':
        return get_errors(id)

    elif request.method == 'PUT':
        line = request.args.get('line', '')
        name = request.args.get('name', '')
        description = request.args.get('description', '')
        return updateError(id, line, name, description)

    elif request.method == 'DELETE':
        return deleteAnError(id)


if __name__ == "__main__":
    app.run(debug=True)
