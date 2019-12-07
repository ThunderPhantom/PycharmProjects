from flask import Flask
from flask import render_template, request, redirect, session, flash
from flask import request
from flask_moment import Moment
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
app = Flask('UserAccounts')
Bootstrap(app)
moment = Moment(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/UserAccounts'
mongo = PyMongo(app)
collection = mongo.db.AccountInformation


@app.route('/')
def registration():
    return render_template('registration.html')

users = {}
@app.route('/registeruser',methods=['POST','GET'])
def registeruser():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']

    users={}
    users = {'first_name': first_name, 'last_name': last_name, 'email': email, 'password': password}

    return redirect('/login')


@app.route('/login', methods = ['GET', 'POST'])
def login():

    return render_template('login.html')

@app.route('/loginuser', methods = ['GET', 'POST'])
def loginuser():
    email = request.form['email']

    password = request.form['password']
    collection = mongo.db.AccountInformation

    user = collection.find_one({'email': email})

    if email not in users:


        return redirect('/invalid')

    elif users[email]['password'] == password:
        session['user'] = users[email]
        return redirect('/home')

    else:

        return redirect('/login')


@app.route('/invalid')
def invalid():
    return render_template('invalid.html')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/login')
    email = session['user']

    collection = mongo.db.AccountInformation

    user = collection.find_one({'email': email})

    first_name = user['first_name']

    return render_template('home.html', current_time=datetime.utcnow(), first_name=first_name)

@app.route('/logout', methods = ['GET','POST'])
def logout():
    del session['user']
    return redirect('/login')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html',error=e)

@app.errorhandler(400)
def bad_request(e):
    return render_template('error400.html',error=e),400


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error500.html',error=e),500



if __name__=='__main__':
    app.run(debug=True)