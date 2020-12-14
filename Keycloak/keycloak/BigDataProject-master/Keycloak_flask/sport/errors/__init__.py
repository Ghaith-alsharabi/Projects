from flask import Blueprint

bp = Blueprint('errors', __name__)

from sport.errors import handlers
