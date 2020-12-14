from flask import Blueprint
import os

bp = Blueprint("renameCsv", __name__)

UPLOAD_FOLDER = 'uploads/sheets'
ALLOWED_EXTENSIONS = {'xlsx', 'csv'}

from sport.renameCsv import routes
