from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from datetime import datetime

@app.route("/")
@app.route("/index")
@login_required
def index():
    user = {'username':'Neeraj'}
    posts = [
        {
            'author':{'username':'Madhukar'},
            'body':{'Flask is great for developing web apps'}
        },
        {
            'author':{'username':'Sunita'},
            'body':{'करडई ची भाजी is awesome!'}
        }
    ]
    return render_template('index.html', title="Home Page", posts=posts)
    # return render_template('index.html', title="", user=user)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password!')
            return redirect(url_for('login'))
        # flash(f'Login requested for user: {form.username.data}, remember_me={form.remember_me.data}')

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your registration is complete.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author':user, 'body':'Test Post # 1'},
        {'author':user, 'body':'Test Post # 2'},
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()