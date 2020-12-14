from flask import  render_template, redirect, url_for, session, request,flash
# import MySQLdb.cursors
from sport.auth import bp
from sport.auth.forms import LoginForm, RegistrationForm
from sport import db
from flask_login import login_user, login_required, logout_user
from sport.models import User
from flask_login import login_user, current_user, logout_user, login_required

from sport import dash_app
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
# from flask_login import login_user, current_user, logout_user, login_required

# from app import app
from sport.basketballApp.basketballDashboard.basketballApps import (
    overview,
    loadManagement,
    compose,
    comparison,
    select,
)  # , shooting


test = current_user

def change_layout(basketball_app,players,role): 
    if  role == "Coach":
        basketball_app.layout = html.Div(
        children=[
            html.H5("Orange Lions 3x3 Basketball", style={"textAlign": "center"}),
            dcc.Tabs(   
                [
                    dcc.Tab(
                        label="Overview",
                        children=[
                            overview.get_overview_layout(basketball_app,players),
                        ],
                    ),
                    dcc.Tab(
                        label="Load Management",
                        children=[
                            loadManagement.get_loadManagement_layout(basketball_app,players),
                        ],
                    ),
                    dcc.Tab(
                        label="Compose",
                        children=[
                            compose.get_compose_layout(basketball_app,players),
                        ],
                    ),
                    dcc.Tab(
                        label="Select",
                        children=[
                            select.get_select_layout(basketball_app,players),
                        ],
                    ),
                    dcc.Tab(
                        label="Session Comparison",
                        children=[
                            comparison.get_comparison_layout(basketball_app,players),
                        ],
                    ),
                ]
            )
        ])
    elif role == "Player":
        basketball_app.layout = html.Div(children=[
            html.H5("Orange Lions 3x3 Basketball", style={"textAlign": "center"}),
            dcc.Tabs(   
                [
                    dcc.Tab(
                        label="Overview",
                        children=[
                            overview.get_overview_layout(basketball_app,players),
                        ],
                    ),
                    dcc.Tab(
                        label="Load Management",
                        children=[
                            loadManagement.get_loadManagement_layout(basketball_app,players),
                        ],
                    ),
                    dcc.Tab(
                        label="Compose",
                        children=[
                            compose.get_compose_layout(basketball_app,players),
                        ],
                    ),
                    dcc.Tab(
                        label="Session Comparison",
                        children=[
                            comparison.get_comparison_layout(basketball_app,players),
                        ],
                    ),
                ]
            )
        ])



@bp.route("/",methods=['POST','GET'])
@bp.route("/login",methods=['POST','GET'])
def login():
    

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # print(user.role)
        # print(current_user)
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
                    #  Import Dash application
            if user.role == "Coach":
                players = ['Kiki FLEUREN', 'Zoë SLAGTER', 'Fleur KUIJT', 'Karin KUIJT',
                        'Richelle VAN DER KEIJL', 'Esther FOKKE', 'Noor DRIESSEN', 'Loyce BETTONVIL',
                        'Ilse KUIJT', 'Jill BETTONVIL', 'Emese HOF', 'Natalie VAN DEN ADEL',
                        'Jacobien KLERX', 'Charlotte VAN KLEEF', 'Rowie JONGELING', 'Janine Guijt', 'Sonja Kuijt', 'Alina SENDAR']

                change_layout(dash_app.app,players,role=user.role)
            elif user.role == "Player":
                players =[str(form.username.data)]

                change_layout(dash_app.app,players,role=user.role)

            return redirect('dashboard')
        else:
            print("not good")
            flash("Invalid username or password")
            return redirect(url_for('auth.login'))

        # if user and bcrypt.check_password_hash(user.password, form.password.data):
        #     login_user(user, remember=form.remember.data)
        #     return redirect(url_for('role.roles'), )
    return render_template('auth/inlog.html', form=form)
    
# Login logic

@bp.route("/register", methods=['GET', 'POST'])
def Register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', title='Register',
                           form=form)

    # form = LoginForm()
    # if form.validate_on_submit():
    #     hashed_password = bcrypt.generate_password_hash(
    #         form.password.data).decode('utf-8')
    #     user = User(username=form.username.data, email=form.email.data, phone=form.phone.data, password=hashed_password,
    #                 auth_mode=form.authentication.data, valid_ip=request.remote_addr+" ")
    #     db.session.add(user)
    #     db.session.commit()
    # return render_template('auth/signup.html', form=form)


# @bp.route("/home")
# @login_required
# def home():
#     return render_template('auth/home.html')#, username=session['username'])



@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 



current_user = current_user