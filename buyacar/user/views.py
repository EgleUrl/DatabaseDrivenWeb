from flask import render_template, request, Blueprint, session, redirect, url_for, flash
from buyacar.models import db, Car, Client, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user


# Creates blueprint for admin
users = Blueprint('users', __name__)

@users.route("/login", methods=['GET','POST'])
def login():
    # Creates new admin user with name admin and hashed password admin123
    #password = 'admin123'
    #name = 'admin1'
    #newuser = User(name=name, password=generate_password_hash(password, method='pbkdf2'))
    # Adds the new user to the database
    #db.session.add(newuser)
    #db.session.commit()
    # Gathers entered name and password 
    name = request.form.get('name')
    password = request.form.get('password')
    # Filters User database to find the user name
    user = User.query.filter_by(name=name).first()
    # Checks if user with that name or password was found
    if not user or not check_password_hash(user.password, password):  
        if request.method == 'POST':      
            flash('Please check your login details and try again.')
        return render_template('login.html') # if the user doesn't exist or password is wrong, reloads the page
    # Grabs logged user id
    login_user(user)
    return redirect(url_for('admin.index'))

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))