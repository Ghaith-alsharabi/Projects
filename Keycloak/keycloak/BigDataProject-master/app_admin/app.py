#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import pandas as pd
import plotly
import plotly.graph_objs as go
import pandas as pd
import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, \
    check_password_hash
from flask_login import LoginManager, UserMixin, login_user, \
    login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://root:Welkom01!@localhost/flask'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    admin = db.Column(db.Boolean(15), unique=True)

    # email = db.Column(db.String(50), unique=True)

    password = db.Column(db.String(80))
    role = db.Column(db.String(80))


class Role(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(250), unique=True)

    # email = db.Column(db.String(50), unique=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):

    username = StringField('username', validators=[InputRequired(),
                                                   Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(),
                                                     Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):

    # email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])

    username = StringField('username', validators=[InputRequired(),
                                                   Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(),
                                                     Length(min=8, max=80)])


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('roles'))
    else:
        admin = False
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    admin = user.admin
                    if admin == True:
                        return redirect(url_for('roles'))
                    else:
                        return '<h1>Invalid Rights of the User contact local administrator</h1>'
                else:
                    return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,
                                                 method='sha256')
        new_user = User(username=form.username.data,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'

        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/roles')
def roles():
    df = pd.DataFrame()

    if current_user.is_authenticated and current_user.admin == True :
        print(current_user.admin)
        all_data = User.query.all()

        role = Role.query.all()
        return render_template('roles.html', employees=all_data, role=role,)
    else:
        return '<h1>Sign in to acces page</h1>'

@app.route('/insert', methods=['POST'])
def insert():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        hashed_password = generate_password_hash(password,
                                                 method='sha256')

        new_user = User(username=username, password=hashed_password,
                        role=role)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('roles'))


# this is our update route where we are going to update our employee

@app.route('/update', methods=['GET', 'POST'])
def update():
    print('role', request.form['role'])

    if request.method == 'POST':
        my_data = User.query.get(request.form.get('id'))

        my_data.username = request.form['username']
        my_data.role = request.form['role']

        db.session.commit()

        return redirect(url_for('roles'))


# This route is for deleting our employee

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('roles'))


@app.route('/overview')
def overview():
    if current_user.is_authenticated and current_user.admin == True :
        df = pd.read_csv("df.csv")
        x = df['names']
        y = df['values']
        bar = create_plotRoles(x, y)

        users = User.query.all()
        x = []
        y = []
        for user in users:
            x.append(user.id)
            y.append(user.role)

        #x,y = all_data.id, all_data.role
        bar2 = create_plotCRoles(x, y)

        countUsers = User.query.count()
        countRoles = Role.query.count()

        return render_template('overview.html', plot=bar, plot2=bar2, countR=countRoles, countU=countUsers)
    else:
        return '<h1>Sign in to acces page</h1>'


def create_plotRoles(x, y):

    df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe
    data = [
        go.Bar(
            x=df['x'],  # assign x as the dataframe column 'x'
            y=df['y'],
            marker_color='LightSkyBlue',
            name="Beschikbare gebruikers",

        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_plotCRoles(x, y):
    coordinator = 0
    trainer = 0
    administrator = 0
    coach = 0
    overig = 0
    for user in y:
        if ("Coordinator" in str(user)):
            coordinator += 1
        elif ("Trainer" in str(user)):
            trainer += 1
        elif ("Administrator" in str(user)):
            administrator += 1
        elif ("Coach" in str(user)):
            coach += 1
        else:
            overig += 1

    names = ['Coordinator', 'Trainer', 'Administrator', 'Coach', 'Overig']
    values = [coordinator, trainer, administrator, coach, overig]

    df = pd.DataFrame({'x': names, 'y': values})  # creating a sample dataframe
    data = [
        go.Bar(
            x=df['x'],  # assign x as the dataframe column 'x'
            y=df['y'],
            marker_color='MediumPurple',
            name="Actieve gebruikers",


        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


if __name__ == '__main__':
    app.run(debug=True)
