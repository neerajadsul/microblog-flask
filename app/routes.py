from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route("/")
@app.route("/index")
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
    return render_template('index.html', title="Home Page", user=user, posts=posts)
    # return render_template('index.html', title="", user=user)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user: {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)