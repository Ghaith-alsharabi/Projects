from flask import  render_template, redirect, url_for, session, request,flash
# import MySQLdb.cursors
from sport.auth import bp
from sport.auth.forms import LoginForm, RegistrationForm
from sport import db
from flask_login import login_user, login_required, logout_user
from sport.models import User

@bp.route("/",methods=['POST','GET'])
@bp.route("/login",methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('role.roles'))
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


@bp.route("/home")
@login_required
def home():
    return render_template('auth/home.html')#, username=session['username'])



@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 
