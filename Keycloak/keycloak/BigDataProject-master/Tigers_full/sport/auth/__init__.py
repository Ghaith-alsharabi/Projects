from flask import Blueprint

bp = Blueprint('auth', __name__)

from sport.auth import routes