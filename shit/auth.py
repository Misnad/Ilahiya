from flask import Blueprint, render_template, url_for, request, redirect, flash
from . import db
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
import random
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.salted_pass, password + user.username):
                flash("logged in", category='success')
                login_user(user, remember=True)
                return redirect(url_for('view.home'))
            else:
                flash("Incorrect password", category='error')
        else:
            flash('E-mail does not exit. Please create an account first.', category='error')
    return render_template('login.html', theme="light", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('view.home'))


@auth.route('/newuser', methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['new_name']
        email = request.form['new_email']
        username = name + "@" + (str)(random.randint(1000, 9999))
        while bool(Users.query.filter_by(username=username).first()):
            username = name + "@" + (str)(random.randint(1000, 9999))

        # Salt = username
        password = generate_password_hash(request.form['password'] + username, method='sha256')

        if len(name) < 4:
            flash("Enter name with atleast 4 characters.", category='error')
        elif len(password) < 6:
            flash("Password must have atleast 6 characters.", category='error')
        elif len(email) < 3 or '@' not in email or '.' not in email or ' ' in email:
            flash("Enter a valid email.", category='error')
        elif Users.query.filter_by(email = email).first():
            flash("An account with the same email exists. Use login.", category='error')
        else:
            flash("Account created!", category='success')
            db.session.add(Users(name=name, email=email, username=username, salted_pass=password))
            db.session.commit()
            return redirect(url_for("auth.login"))

    return render_template('newuser.html', theme="light", user=current_user)
