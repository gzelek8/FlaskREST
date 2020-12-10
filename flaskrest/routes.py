from flask import render_template, url_for, flash, redirect, request
from flaskrest import app, db, bcrypt
from flaskrest.forms import RegistrationForm, LoginForm, EditProfileForm
from flaskrest.models import User, UnityError
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('showErrors'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('showErrors'))


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route("/account/<username>")
@login_required
def account(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('account.html', user=user, posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route('/')
@app.route('/errors')
def showErrors():
    errors = db.session.query(UnityError).all()
    return render_template('home.html', errors=errors)


@app.route('/errors/new/', methods=['GET', 'POST'])
def newError():
    if request.method == 'POST':
        newError = UnityError(line=request.form['line'],
                              name=request.form['name'],
                              description=request.form['description'])
        db.session.add(newError)
        db.session.commit()
        return redirect(url_for('showErrors'))
    else:
        return render_template('newError.html')


@app.route("/errors/<int:error_id>/edit/", methods=['GET', 'POST'])
def editError(error_id):
    editedError = db.session.query(UnityError).filter_by(id=error_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedError.description = request.form['name']
            return redirect(url_for('showErrors'))
    else:
        return render_template('editError.html', error=editedError)


@app.route('/errors/<int:error_id>/delete/', methods=['GET', 'POST'])
def deleteError(error_id):
    errorToDelete = db.session.query(UnityError).filter_by(id=error_id).one()
    if request.method == 'POST':
        db.session.delete(errorToDelete)
        db.session.commit()
        return redirect(url_for('showErrors', error_id=error_id))
    else:
        return render_template('deleteError.html', error=errorToDelete)


"""
api functions
"""
from flask import jsonify


def get_errors():
    errors = db.session.query(UnityError).all()
    return jsonify(errors=[x.serialize for x in errors])


def get_error(error_id):
    errors = db.session.query(UnityError).filter_by(id=error_id).one()
    return jsonify(errors=errors.serialize)


def makeANewError(line, name, description):
    addederror = UnityError(line=line, name=name, description=description)
    db.session.add(addederror)
    db.session.commit()
    return jsonify(UnityError=addederror.serialize)


def updateError(id, line, name, description):
    updatedError = db.session.query(UnityError).filter_by(id=id).one()
    if not line:
        updatedError.line = line
    if not name:
        updatedError.name = name
    if not description:
        updatedError.description = description
    db.session.add(updatedError)
    db.session.commit()
    return 'Updated a Error with id %s' % id


def deleteAnError(id):
    errorToDelete = db.session.query(UnityError).filter_by(id=id).one()
    db.session.delete(errorToDelete)
    db.session.commit()
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
