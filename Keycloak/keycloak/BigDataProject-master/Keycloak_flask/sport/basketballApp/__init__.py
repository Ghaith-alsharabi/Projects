from flask import Blueprint

bp = Blueprint("basketballApp", __name__)

from sport.basketballApp import routes
