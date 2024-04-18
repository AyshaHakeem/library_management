from flask import Blueprint, redirect, render_template, request, url_for, jsonify, flash
from library_flask import db, bcrypt
from flask_login import login_required, current_user, login_user, logout_user
from library_flask.models import User

users = Blueprint('users', __name__)

@users.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('users.display_dashboard'))
    else:
        return redirect(url_for('users.sign_up'))

@users.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("sign-up.html")
    
    data = request.form  
    filter_criteria = {'email': data['userEmail']}
    user = User.query.filter_by(**filter_criteria).first()
    if not user:
        hashed_password = bcrypt.generate_password_hash(data['userPassword']).decode('utf-8')
        try:
            new_user = User(
                fullname=data['userFullName'],
                email=data['userEmail'], 
                password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('signup successful')
            return redirect(url_for('users.login'))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        flash('User with the same email id already exists', 'error')  
        return render_template("sign-up.html")

@users.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        filter_criteria = {'email': data['userEmail']}
        user = User.query.filter_by(**filter_criteria).first()
        if user and bcrypt.check_password_hash(user.password, data['userPassword']):
            login_user(user)
            return redirect(url_for('users.display_dashboard'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'error')
    return render_template("login.html")


@users.route("/logout")
def logout():
    logout_user()
    flash('User logged out')
    return redirect(url_for('users.home'))

@users.route("/dashboard")
@login_required
def display_dashboard():
    return render_template('home.html')

