import os, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO

# from OpenSSL import SSL
# import os

# context = SSL.Context(SSL.SSLv23_METHOD)
# cer = os.path.join(os.path.dirname(__file__), '/usr/local/bin/flask/flask_app/963.crt')
# key = os.path.join(os.path.dirname(__file__), '/usr/local/bin/flask/flask_app/963.key')


app = Flask(__name__)
app.config['SECRET_KEY'] = '5291628bb0513ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.refresh_view='relogin'
login_manager.needs_refresh_message='Session timeout, please re-login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_ASCII_ATTACHMENTS ']=True



if sys.platform == "win32":
    app.config['MAIL_USERNAME'] = os.environ.get('Unit_UN')
    app.config['MAIL_PASSWORD'] = os.environ.get('Unit_PW') #Unit@2021
    app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get('Public_Rec') #6Lex2uoUAAAAAAb5gq3GW6giqZILwPDf3Ta1Dz1n
    app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('Private_Rec') #6Lex2uoUAAAAALWw9QHWk3dASNOaRpBNCiofALI9
    account_sid = os.environ.get('sms_id') #AC3244630a036fdf49565017fd0b5b66de
    auth_token = os.environ.get('sms_key') #ecd9b562c5e3fa01e94d4486d5f0ddf7
    map_token = os.environ.get('map_token') #AIzaSyBmkr9NSYs9917rlJL2Z-RMrmkPDpEB1T4

else:
    print("other OS")
    print(sys.platform)

mail = Mail(app)
socketio = SocketIO(app)

from MFA import routes