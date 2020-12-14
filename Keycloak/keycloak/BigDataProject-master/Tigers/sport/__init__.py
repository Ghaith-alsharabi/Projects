from flask import Flask
from flask_mysqldb import MySQL , MySQLdb
#import bcrypt

app = Flask(__name__)
#app.config['SECRET_KEY'] = '4ddf8a374af1d4c912235859fb715b27'
app.config['MYSQL_HOST'] = '' # the host name
app.config['MYSQL_USER'] = '' # the user (root)
app.config['MYSQL_PASSWORD'] = '' # the password 
app.config['MYSQL_DB'] = '' # the name of the database
#app.config['MYSQL_CURSORCLASS'] = 'DictCursour'
db=MySQL(app)

from sport import routes