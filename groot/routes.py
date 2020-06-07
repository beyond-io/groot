from flask import Flask, Response, render_template, request, redirect, url_for, flash, abort
from run import app, db
from groot.models import *
from flask_login import login_user, current_user, logout_user, login_required
import hashlib


@app.route("/")
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            if current_user.is_authenticated:
                return redirect(url_for('dashboard'))
            user_data = request.form.to_dict()
            if is_user_data_valid(user_data):
                user = User.query.filter_by(email=user_data['email']).first()
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            return redirect(url_for('login'))  
        except:
            abort(404)
    else:
        return render_template('login.html')



def is_user_data_valid(user_data):
    user = User.query.filter_by(email=user_data['email']).first()
    if not user:
        flash('Inccorect email! Please try again.', 'danger')
        return False
    if user.password != create_encrypted_password(user_data['password']):
        flash('Inccorect password! Please try again.', 'danger')
        return False    
    return True



@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            if current_user.is_authenticated:
                return redirect(url_for('dashboard'))
            user_data = request.form.to_dict()
            user_data['password'] = create_encrypted_password(user_data['password'])
            save_user_to_database(user_data)
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        except:
            abort(404, description="Unknown error occured")
    else:
        return render_template('register.html')


def create_encrypted_password(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()


def save_user_to_database(user_data):
    user = User(email=user_data['email'],first_name=user_data['first_name'],
                last_name=user_data['last_name'],nick_name=user_data['nick_name'],
                password=user_data['password'])
    db.session.add(user)
    db.session.commit()


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('index.html', title='Dashboard')


@app.route('/policies', methods=['GET', 'POST'])
@login_required
def policies():
    return render_template('policies.html', title='Policies')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', title='Profile')


@app.route('/sensors', methods=['GET', 'POST'])
@login_required
def sensors():
    return render_template('sensors.html', title='Sensors')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
	