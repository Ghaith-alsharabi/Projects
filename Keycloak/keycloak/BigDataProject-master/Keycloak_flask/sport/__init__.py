from flask import Flask
from flask_mysqldb import MySQL , MySQLdb
from flask_login import LoginManager
from flask_babel import Babel, lazy_gettext as _l
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy  import SQLAlchemy
from flask_bcrypt import Bcrypt




# bootstrap = Bootstrap()
# # bcrypt = Bcrypt()
# db = SQLAlchemy()
# login_manager = LoginManager()
# login_manager.login_view = 'login'
# #assets = Environment()



# def create_app(config_class=Config):
#     app = Flask(__name__)
#     # app = Flask(__name__, instance_relative_config=False)
#     #app.config.from_object("config.Config")

#     app.config.from_object(config_class)
#     app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ghaith099@localhost/flask'
#     login_manager.init_app(app)
#     # bcrypt.init_app(app)
#     db.init_app(app)
#     bootstrap.init_app(app)
#     #assets.init_app(app)
#     #migrate.init_app(app, db)



#     with app.app_context():
#         db.create_all()


#     from sport.errors import bp as errors_bp
#     app.register_blueprint(errors_bp)

#     from sport.rolen import bp as role_bp
#     app.register_blueprint(role_bp)

#     from sport.auth import bp as auth_bp
#     app.register_blueprint(auth_bp)#, url_prefix='/auth')

#     from sport.main import bp as main_bp
#     app.register_blueprint(main_bp)
    
#     return app




import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_assets import Environment
from config import Config

from flask_oidc import OpenIDConnect

class DashApp:
    def __init__(self,app=None):
        self.app = app
    def init_app(self,app):
        self.app = app




dash_app = DashApp()

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'login'

oidc = OpenIDConnect()

def create_app(config_class=Config):

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    assets = Environment()
    app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ghaith099@localhost/flask'
    login_manager.init_app(app)
    app.config.update({
        'SECRET_KEY': 'SomethingNotEntirelySecret',
        'TESTING': True,
        'DEBUG': True,
        'OIDC_CLIENT_SECRETS': 'C:/client_secrets.json',
        'OIDC_ID_TOKEN_COOKIE_SECURE': False,
        'OIDC_REQUIRE_VERIFIED_EMAIL': False,
        'OIDC_VALID_ISSUERS': ['http://localhost:8080/auth/realms/demo'],
        'OIDC_OPENID_REALM': 'http://localhost:5000/oidc_callback',
        'OIDC_SCOPES': ['openid', 'email', 'roles']
        # 'OIDC_TOKEN_TYPE_HINT': 'access_token'
    })


    assets.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    oidc.init_app(app)

    with app.app_context():
        # Import parts of our core Flask app
        from .basketballApp import routes
        from .basketballApp.assets import compile_static_assets

        #  Import Dash application
        from .basketballApp.basketballDashboard.basketballDashboardApp import (
            init_dashboard,
        )

        dashboard = init_dashboard(app)
        dash_app.init_app(dashboard)

        # Compile static assets
        compile_static_assets(assets)

        from sport.renameCsv import bp as rename_csv_bp
        app.register_blueprint(rename_csv_bp, url_prefix="/renameCsv")

        from sport.basketballApp import bp as basketball_app_bp
        app.register_blueprint(basketball_app_bp)

        
        from sport.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

        from sport.adminFilePage import bp as admin_bp
        app.register_blueprint(admin_bp)

        from sport.auth import bp as auth_bp
        app.register_blueprint(auth_bp)#, url_prefix='/auth')

        from sport.main import bp as main_bp
        app.register_blueprint(main_bp)


        if not app.debug and not app.testing:

            if not os.path.exists("logs"):
                os.mkdir("logs")
            file_handler = RotatingFileHandler(
                "logs/wsgi.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s "
                    "[in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info("wsgi startup")

        return app

