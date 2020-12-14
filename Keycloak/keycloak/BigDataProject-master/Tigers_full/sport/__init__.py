from flask import Flask
from flask_mysqldb import MySQL , MySQLdb
from flask_login import LoginManager
from flask_babel import Babel, lazy_gettext as _l
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy  import SQLAlchemy
from flask_bcrypt import Bcrypt




bootstrap = Bootstrap()
# bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ghaith099@localhost/flask'
    login_manager.init_app(app)
    # bcrypt.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    with app.app_context():
        db.create_all()


    from sport.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from sport.rolen import bp as role_bp
    app.register_blueprint(role_bp)

    from sport.auth import bp as auth_bp
    app.register_blueprint(auth_bp)#, url_prefix='/auth')

    from sport.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app