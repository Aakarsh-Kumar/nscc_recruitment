from datetime import datetime
from flask_login.utils import login_required, login_user, logout_user, current_user
from db import save_user,get_user
from user import User
from flask import Flask, render_template, redirect, request, url_for,session, abort, make_response
from flask_login import LoginManager
from pymongo.errors import DuplicateKeyError
import os


app = Flask(__name__,template_folder='templates')

app.secret_key = "0128d79584ś614d4e92b42cb07032bb0e"

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

@app.route('/',methods=['GET','POST'])
def index():
    if current_user.is_authenticated:
        return str(current_user.name)
    if request.method=='POST':
        email=request.form.get('email')
        name=request.form.get('name')
        password=request.form.get('password')
        if 'name' in request.form:
            save_user(email,name,password)
        else:
            if get_user(email,password):
               login_user(User(email,name))
               session['email']=email
               return redirect('/')
            else:
                return render_template('index.html',message='Invalid credentials!')
    return render_template('index.html')

@login_manager.user_loader
def load_user(email):
    return User(session['email'],session['name'])

#------Logout the user-----------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=5000)