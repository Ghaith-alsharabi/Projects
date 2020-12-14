from flask import render_template, url_for, flash, redirect, abort, session, request
from MFA import app, db, bcrypt, mail, socketio
from MFA.forms import RegistrationForm, LoginForm, RequestVerifyEmail, ResetPassword, QRForm, TakePhoto, SMSForm
from MFA.models import User
from datetime import timedelta
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flask_socketio import emit
import time


@app.before_request
def before_request():
    session.permanent = True
    # can be changed after test
    app.permanent_session_lifetime = timedelta(minutes=1)


def stay_in_your_auth_mode(auth_mode):
    if auth_mode == 'Face':
        return redirect(url_for('face_confirm'))
    elif auth_mode == 'QR':
        return redirect(url_for('qr_confirm'))
    elif auth_mode == 'SMS':
        return redirect(url_for('sms'))


# {url_for('confirm_email', token=token, _external=True)}

def send_confirmation_email(user):
    token = user.create_token()
    msg = Message('Email address confirmation',
                  sender='unit963.hva@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To confirm your E-mail click on the following link:
http://127.0.0.1:5000/confirm_email/{token}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def send_reset_password(user):
    token = user.create_token()
    msg = Message('Reset Password Link',
                  sender='unit963.hva@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password click on the following link:
{url_for('reset_password', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/")
@app.route("/home")
@login_required
def home():
    if current_user.authenticated:
        return render_template('home.html', title='Home Page')
    else:
        return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.authenticated:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, phone=form.phone.data, password=hashed_password,
                    auth_mode=form.authentication.data, valid_ip=request.remote_addr+" ")

        user.time_out = False
        user.check_time = "0"
        user.face_confirmed = False
        user.authenticated = False
        user.oneTime_reg = False

        db.session.add(user)
        db.session.commit()
        if user.auth_mode == 'QR':
            # user.face_confirmed = True
            # user.sms_confirmed = True
            user.create_qr()
            db.session.commit()
            session['dump_qr'] = user.id
            try:
                send_confirmation_email(user)
                flash(
                    'Email has been sent to verify your account! Verify it to be able to log in', 'success')
            except:
                flash(
                    'Email sending failed.. Click on verify Email below to get email again', 'info')
            return redirect(url_for('qr'))

        elif form.authentication.data == 'SMS':
            user.auth_mode = "SMS"
           # user.face_confirmed = True
            # user.qr_confirmed = True
            db.session.commit()
            try:
                send_confirmation_email(user)
                flash(
                    'Email has been sent to verify your account! Verify it to be able to log in', 'success')
            except:
                flash(
                    'Email sending failed.. Click on verify Email below to get email again', 'info')
            return redirect(url_for('login'))

        else:
            user.auth_mode = "Face"
            # user.qr_confirmed = True
            # user.sms_confirmed = True
            db.session.commit()
            session['dump_face'] = user.id
            try:
                send_confirmation_email(user)
                flash(
                    'Email has been sent to verify your account! Verify it to be able to log in', 'success')
            except:
                flash(
                    'Email sending failed.. Click on verify Email below to get email again', 'info')
            return redirect(url_for('take_photo'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.authenticated:
        return redirect(url_for('home'))
    else:
        form = LoginForm()

        logout_user()

        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                if request.remote_addr in user.valid_ip:
                    if user.confirmed_email:
                        login_user(user, remember=form.remember.data)
                        user.authenticated = False
                        if user.auth_mode == "QR":
                            user.qr_confirmed = False
                            db.session.commit()
                            return redirect(url_for('qr_confirm'))
                        elif user.auth_mode == "Face":
                            user.time_out = False
                            user.check_time = "0"
                            user.face_confirmed = False
                            user.authenticated = False
                            user.oneTime_reg = False
                            db.session.commit()
                            return redirect(url_for('face_confirm'))
                        elif user.auth_mode == "SMS":
                            user.sms_confirmed = False
                            user.send_sms()
                            return redirect(url_for('sms'))
                    else:
                        flash(
                            'Verify your E-mail first to be able to login', 'danger')
                else:
                    device = request.user_agent.platform
                    browser = request.user_agent.browser
                    ver = request.user_agent.version
                    user.send_security_email(
                        request.remote_addr, device, browser, ver)
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        return render_template('login.html', title='Login', form=form)


@app.route("/save_ip/<email>/<token>/<ip>", methods=['GET', 'POST'])
def save_ip(email, token, ip):
    email = email
    token = token
    ip = ip
    user = User.query.filter_by(email=email).first()
    if ip in user.valid_ip:
        pass
    else:
        user.valid_ip += (ip + " ")
        user.rem_token = None
        db.session.commit()
    flash("Your IP address has been saved", "success")
    return render_template('add_ip.html', ip=ip)


@app.route("/sms", methods=['GET', 'POST'])
@login_required
def sms():
    if current_user.auth_mode != "SMS":
        return stay_in_your_auth_mode(current_user.auth_mode)

    form = SMSForm()
    if form.validate_on_submit():
        enteredKey = form.sms_code.data
        if enteredKey == current_user.sms_code:
            current_user.sms_confirmed = True
            current_user.authenticated = True
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flash('SMS code is incorrect', 'danger')
    return render_template("sms_conf.html", title="SMS Verification", form=form)


@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated or current_user.authenticated:
        if current_user.auth_mode == "QR":
            current_user.qr_confirmed = False
        elif current_user.auth_mode == "Face":
            current_user.face_confirmed = False
        elif current_user.auth_mode == "SMS":
            current_user.sms_confirmed = False
        session.clear()
        current_user.authenticated = False
        db.session.commit()
        logout_user()
    return redirect(url_for('login'))


@app.route("/confirm_email/<token>", methods=['GET', 'POST'])
def confirm_email(token):
    user = User.verify_token(token)
    try:
        if not user:
            abort(404)
        elif user.confirmed_email:
            flash('Your email is already confirmed', 'info')
            return redirect(url_for('login'))
        else:
            user.confirmed_email = True
            db.session.commit()
            flash('Email Confirmed.. now you can login', 'success')
    except AttributeError:
        abort(404)
    return render_template('confirm_email.html')


@app.route("/request_verify_email", methods=['GET', 'POST'])
def request_verify_email():
    form = RequestVerifyEmail()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.confirmed_email:
                flash('Your Email is already verified.', 'success')
                return redirect(url_for('login'))
            else:
                send_confirmation_email(user)
                flash('Confirmation Email has been sent.', 'success')
                return redirect(url_for('login'))
        else:
            flash('Email not found', 'danger')
            return redirect(url_for('register'))
    return render_template('request_verify_email.html', title='Verify Email address', form=form)


@app.route("/request_reset_password", methods=['GET', 'POST'])
def request_reset_password():
    form = RequestVerifyEmail()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_password(user)
            flash('Email with reset link has been sent', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email not found', 'danger')
            return redirect(url_for('register'))
    return render_template('request_reset_password.html', title='Request Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPassword()
    user = User.verify_token(token)
    try:
        if not user:
            abort(404)
        else:
            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(
                    form.password.data).decode('utf-8')
                user.password = hashed_password
                db.session.commit()
                flash('Password has been reset', 'success')
                return redirect(url_for('login'))
    except AttributeError:
        abort(404)
    return render_template('reset_password.html', title='Reset Password', form=form)


@app.route("/qr", methods=['GET', 'POST'])
def qr():
    if current_user.auth_mode != "QR":
        return stay_in_your_auth_mode(current_user.auth_mode)
    if current_user.is_authenticated and current_user.authenticated:
        print("logged_in")
        return render_template('qr.html', title='QR Code', id=current_user.id)
    else:
        try:
            if session['dump_qr']:
                id = session['dump_qr']
                session.clear()
                return render_template('qr.html', title='QR Code', id=id)
        except:
            return redirect(url_for('register'))
    return render_template('qr.html', title='QR Code')


@app.route("/qr_confirm", methods=['GET', 'POST'])
@login_required
def qr_confirm():
    if current_user.auth_mode != "QR":
        return stay_in_your_auth_mode(current_user.auth_mode)

    user = User.query.filter_by(id=current_user.id).first()
    if user.authenticated:
        return redirect(url_for('home'))
    form = QRForm()
    user = User.query.filter_by(id=current_user.id).first()
    dump = str(user.verify_qr())
    if form.validate_on_submit():
        if form.qr_code.data == dump:
            user.qr_confirmed = True
            user.authenticated = True
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flash('Incorrect passcode Try Again', 'danger')
    return render_template('qr_confirm.html', title='QR Confirm', form=form)


@app.route("/save_photo", methods=['POST', 'GET'])
def save_photos():
    img = request.form.get("content").split(',')[1]
    try:
        if current_user.is_authenticated and current_user.auth_mode == "Face":
            user = User.query.filter_by(id=current_user.id).first()
            user.create_photo(id=user.id, img=img)
    except:
        if session['dump_face']:
            user = User.query.filter_by(id=session['dump_face']).first()
            id = user.id
            user.create_photo(id=id, img=img)
            print("done")

    return "got it"


@app.route("/take_photo", methods=['POST', 'GET'])
def take_photo():
    form = TakePhoto()
    try:
        if current_user.is_authenticated and current_user.auth_mode == "Face":
            if form.validate_on_submit():
                return redirect(url_for('face_confirm'))
            return render_template('take_photo.html', title='Take Photo', form=form)
        elif session['dump_face']:
            if form.validate_on_submit():
                return redirect(url_for('login'))
            return render_template('take_photo.html', title='Take Photo', form=form)
    except:
        return redirect(url_for('register'))


@socketio.on('image', namespace='/processing')
@login_required
def handle_my_custom_namespace_event(image):
    if current_user.is_authenticated:
        # now = datetime.datetime.now()
        millisec = int(round(time.time() * 1000))
        user = User.query.filter_by(id=current_user.id).first()
        face_check = user.image_processing(img=str(image).split(',')[1])

        if face_check:
            user.face_confirmed = True
            user.authenticated = True
            db.session.commit()
            user.send_logo("success")
            time.sleep(1)
            if not user.oneTime_reg:
                print("send")
                emit('response', "find")
                current_user.oneTime_reg = True
                db.session.commit()
        elif face_check == False:
            user.send_logo("failed")
            user.face_confirmed = False
            db.session.commit()

        # start timer
        if user.check_time == "0":
            user.check_time = str(millisec)
            db.session.commit()
        # # 120000 milliseconds means 2 min
        elif int(current_user.check_time) + 12000 < millisec:
            print('timeOut')
            user.time_out = True
            user.check_time = "0"
            user.face_confirmed = False
            db.session.commit()
            emit('response', "refresh")


@app.route("/face_confirm", methods=['POST', 'GET'])
@login_required
def face_confirm():
    if current_user.auth_mode != "Face":
        return stay_in_your_auth_mode(current_user.auth_mode)

    if current_user.is_authenticated:
        try:
            if current_user.time_out:
                flash('Login again! \nPage timeout!', 'danger')
                current_user.time_out = False
                current_user.check_time = "0"
                current_user.face_confirmed = False
                current_user.authenticated = False
                db.session.commit()
                logout_user()
                return redirect(url_for('login'))

            elif current_user.face_confirmed:
                current_user.is_authenticated = True
                db.session.commit()

                flash('Your face is confirmed', 'success')
                return redirect(url_for('home'))

            return render_template('face_confirm.html', title='Face Recognition')
        except:
            return redirect(url_for('register'))
    else:
        return redirect(url_for('login'))
