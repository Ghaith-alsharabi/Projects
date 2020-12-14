from flask import render_template, redirect, url_for,request
from flask_login import login_required, logout_user, current_user
from sport import db, login_manager
from sport.rolen import bp
from sport.models import User,Role


# @bp.route('/dashboard')
# @login_required
# def dashboard():
    
#     return render_template('dashboard.html', name=current_user.username)


@bp.route('/roles')
def roles():
    all_data = User.query.all()
    role = Role.query.all()
    return render_template('role/roles.html', employees = all_data, role= role)

@bp.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        user = User.query.filter_by(username=request.form['username']).first()
        if user == None:
            new_user = User(username=request.form['username'], role=request.form['role'])
            new_user.set_password(request.form['password'])
            db.session.add(new_user)
            db.session.commit()

        user1 = User.query.filter_by(username=request.form['username']).first()
        user1.role= request.form['role']
        # user1.password= request.form['password']
        # db.session.add(user1)
        db.session.commit()
  
        return redirect(url_for('role.roles'))
 

#this is our update route where we are going to update our employee
@bp.route('/update', methods = ['GET', 'POST'])
def update():
    #print('role',request.form['role'])
 
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        user.username = request.form['username']
        user.role = request.form.get('role')
        print(request.form.get('role'))
        
        db.session.commit()

 
        return redirect(url_for('role.roles'), )
 
