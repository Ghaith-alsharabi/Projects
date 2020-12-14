from flask import  render_template, redirect, url_for, session, request
from sport import app, db
from sport.forms import LoginForm 
import MySQLdb.cursors


@app.route("/",methods=['POST','GET'])
@app.route("/login",methods=['POST','GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM login WHERE username =%s AND password =%s",(username,password,))
        user = cur.fetchone()
        cur.close()

        if user:
            session['loggedin'] = True
            session['id'] = user ['id']           
            session['username'] = user ['username']
            return render_template('home.html', form=form , Title='Sing In')
        else:
            return render_template('inlogpagina.html', form=form)

    else:
        return render_template('inlogpagina.html', form=form)

    #return render_template('inlogpagina.html', form=form)

@app.route("/home")
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    else:
        return redirect(url_for('login'))    

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login')) 
