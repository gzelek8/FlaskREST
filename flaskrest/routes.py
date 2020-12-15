from flask import render_template, url_for, flash, redirect, request, abort
from flaskrest import app, db, bcrypt, mail
from flaskrest.forms import RegistrationForm, LoginForm, EditProfileForm, PostErrorForm, RequestResetForm, \
    ResetPasswordForm
from flaskrest.models import User, UnityError
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_mail import Message

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


@app.route("/account/<username>")
@login_required
def account(username):
    user = User.query.filter_by(username=username).first_or_404()
    errors = db.session.query(UnityError).filter(UnityError.user_id == user.id)
    return render_template('account.html', user=user, errors=errors)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('account', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route('/')
@app.route('/errors')
def showErrors():
    errors = db.session.query(UnityError).all()
    return render_template('home.html', errors=errors)


@app.route('/errors/<int:error_id>')
def showError(error_id):
    error = UnityError.query.get_or_404(error_id)
    return render_template('error.html', error=error)


@app.route('/<username>/submit', methods=['GET', 'POST'])
@login_required
def newError(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = PostErrorForm()
    if form.validate_on_submit():
        newError = UnityError(line=form.line_nr.data, name=form.error_name.data, description=form.description.data,
                              date_posted=datetime.utcnow(), user_id=user.id)
        db.session.add(newError)
        db.session.commit()
        flash('Your post has been submitted.', 'success')
        return redirect(url_for('showErrors'))
    return render_template('newError.html', form=form, legend='New Error')


@app.route("/errors/<int:error_id>/edit", methods=['GET', 'POST'])
@login_required
def editError(error_id):
    editedError = UnityError.query.get_or_404(error_id)
    if editedError.author != current_user:
        abort(403)
    form = PostErrorForm()
    if form.validate_on_submit():
        editedError.name = form.error_name.data
        editedError.line = form.line_nr.data
        editedError.description = form.description.data
        db.session.commit()
        flash('Your error has been edited!', 'success')
        return redirect(url_for('showError', error_id=editedError.id))
    elif request.method == 'GET':
        form.error_name.data = editedError.name
        form.line_nr.data = editedError.line
        form.description.data = editedError.description
    return render_template('newError.html', form=form, legend='Edit Error')


@app.route('/errors/<int:error_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteError(error_id):
    deletedError = UnityError.query.get_or_404(error_id)
    if deletedError.author != current_user:
        abort(403)
    db.session.delete(deletedError)
    db.session.commit()
    flash('Your error has been deleted!', 'success')
    return redirect(url_for('showErrors'))


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
        line = request.args.get_or_404('line', '')
        name = request.args.get_or_404('name', '')
        description = request.args.get_or_404('description', '')
        return makeANewError(line, name, description)


@app.route('/errorsApi/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def errorFunctionId(id):
    if request.method == 'GET':
        return get_errors(id)

    elif request.method == 'PUT':
        line = request.args.get_or_404('line', '')
        name = request.args.get_or_404('name', '')
        description = request.args.get_or_404('description', '')
        return updateError(id, line, name, description)

    elif request.method == 'DELETE':
        return deleteAnError(id)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Rest Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
    
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

#coment
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to rest your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)
