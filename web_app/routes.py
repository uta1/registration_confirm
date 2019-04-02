from flask import render_template, flash, redirect, url_for, request
from web_app import app, db
from web_app.forms import LoginForm, RegistrationForm, ConfirmationForm
from web_app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from dateutil import parser
from itsdangerous import URLSafeTimedSerializer


from email_notification_sevice.send import sendEmail

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
            {
                'author': {'username': 'John'},
                'body': 'Beautiful day in Portland!'
            },
            {
                'author': {'username': 'Susan'},
                'body': 'The Avengers movie was so cool!'
            }]
    return render_template('index.html', user=user, title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

def deserialize(data):
    serializer = URLSafeTimedSerializer("code".encode('utf8'))
    data = serializer.loads(
        data
    )
    print('pop')
    data[2] = parser.parse(data[2])
    print('lopop')
    return data

def timeIsOk(data):
    print(data)
    return (datetime.utcnow() - data[2]).days < 2

@app.route('/confirm/<code>', methods=['GET', 'POST'])
def confirm(code):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    print('aaa')
    data = deserialize(code)
    print('bbbb')
    if not timeIsOk(data):
        user = User.query.filter_by(username=data[0]).first()
        if user.date_of_reg.date() == parser.parse(data[2].date()):
            user.date_of_reg = datetime.utcnow()
            db.session.commit()
            sendEmail(user)
            flash('We will send you new hash!')
            return redirect(url_for('index'))
        else:
            flash('Wrong date!')
            return redirect(url_for('index'))
    print('kek')	
    form = ConfirmationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=data[0]).first()
        print(user.date_of_reg.date())
        print(datetime.utcnow().date)
        print(data[2].date())
        if user.date_of_reg.date() == data[2].date():
            user.set_password(form.password.data)
            user.isActive = True
            db.session.commit()
            flash('Congratulations, you are registered!')
            return redirect(url_for('login'))
        else:
            flash('Wrong date!')
            return redirect(url_for('index'))
    return render_template('confirm.html', title='Confirm', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@app.route('/del')
def del1():
    User.query.delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, 
        	email=form.email.data, 
        	isActive=False)
        
        db.session.add(user)
        db.session.commit()
        sendEmail(user)
        flash('Congratulations, message with further instructions will be send in one moment!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
