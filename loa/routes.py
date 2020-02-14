from loa import app, db
from flask import render_template, redirect
from loa.forms import RegisterForm, LoginForm
from loa.models import User
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
    
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        hash = generate_password_hash(password)
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered. Please login.')
            return redirect('login')
        else:
            user = User(email=email, hash=hash)
            db.session.add(user)
            db.session.commit()
            return render_template('/login.html')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User does not exist. Please register for an account.')
            return redirect('/register')

        if check_password_hash(user.hash, password):
            flash('Logged in succesfully.')
            redirect('/')
    return render_template('login.html', form=form)
