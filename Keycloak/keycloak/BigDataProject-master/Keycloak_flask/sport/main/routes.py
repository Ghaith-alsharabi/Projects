from flask import  render_template, redirect, url_for, session, request
from sport.main import bp


@bp.route("/main",methods=['POST','GET'])
def main():
    return render_template('index.html')


#  auth_bp = Blueprint(
#   'auth_bp', __name__,
#    template_folder='templates',
#    static_folder='static',)



@bp.route("/test_bp")
def home():
    return "Main folder working with blue print"    
