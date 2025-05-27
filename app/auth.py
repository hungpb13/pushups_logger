from flask import Blueprint, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint("auth", __name__)

@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=['POST'])
def signup_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        print("User already exists!")
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))
    
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/login", methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    print(email, password, remember)

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        print("Email or password is NOT valid!")
        return redirect(url_for('auth.login'))
    
    login_user(user=user, remember=remember)

    return redirect(url_for('main.profile'))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route("/users")
@login_required
def users():
    users = User.query.all()

    return render_template("users.html", users=users)