from flask_app.models import user_model
from flask_app import app, bcrypt
from flask import session, request, render_template, redirect, flash

@app.route('/')
def index():
    if 'uid' in session:
            return redirect('/dashboard')
    return render_template('index.html')

@app.route('/register', methods=["POST"])
def register():
    if not user_model.User.validate_registration(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
        
    data = {
        **request.form,
        "password": pw_hash
    }
    user =  user_model.User.create_user(data)
    print(user)
    session['uid'] =  user
    session['name'] = request.form['first_name']

    if 'uid' not in session:
        flash('Error in account creation.','account')
        session.clear()
        return redirect('/') 
    
    return redirect('/dashboard')

@app.route('/login', methods=["POST"])
def login():
    user_login = user_model.User.validate_login(request.form)
    
    if not user_login:
        flash('Login information is incorrect.','login')
        return redirect('/')
    
    session['uid'] = user_login.id
    session['name'] = user_login.first_name

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()

    return redirect('/')