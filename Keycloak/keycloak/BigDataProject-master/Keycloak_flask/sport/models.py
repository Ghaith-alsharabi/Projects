from flask_login import UserMixin
from sport import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(280))
    role = db.Column(db.String(80))
    # gekozen_role = db.Column(db.String(80))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Role(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(15), unique=True)
    #email = db.Column(db.String(50), unique=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

