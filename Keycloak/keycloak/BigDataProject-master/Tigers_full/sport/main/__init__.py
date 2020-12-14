from flask import Blueprint

bp = Blueprint('main', __name__)

#  auth_bp = Blueprint(
#   'auth_bp', __name__,
#    template_folder='templates',
#    static_folder='static',)

from sport.main import routes