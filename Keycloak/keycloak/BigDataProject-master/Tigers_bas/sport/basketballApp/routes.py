from flask import render_template

from sport.basketballApp import bp
from flask import  render_template, redirect, url_for, session, request,flash
# import MySQLdb.cursors
from sport.auth import bp
# from sport.auth.forms import LoginForm, RegistrationForm
# from sport import db
# from flask_login import login_user, login_required, logout_user
# from sport.models import User
from flask_login import login_user, current_user, logout_user, login_required


@bp.route("/dashboard")
def home():
    if current_user.is_authenticated:
        return render_template(
            "basketballApp/basketball_app.jinja2",
            title="Basketball Dashboard",
            description="Embed Plotly Dash into your Flask applications.",
            template="home-template",
            body="This is a homepage served with Flask.", )

        # return redirect(url_for('basketballApp.basketballDashboard.basketballDashApp'))
    else:
        return redirect(url_for('auth.login'))

