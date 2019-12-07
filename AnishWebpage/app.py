from flask import Flask, render_template, request, redirect, session, flash
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from flask_moment import Moment
from datetime import datetime


a = Flask("mywebsite")
Bootstrap(a)


a.config['MONGO_URI']='mongodb://localhost:27017/mydatabase'
a.config['SECRET_KEY']="fortnite"
mongo=PyMongo(a)
moment = Moment(a)

@a.route("/", methods = ["GET", "POST"])
def display():
    if request.method == "GET":
        return render_template("registrationform.html", current_time = datetime.utcnow())

    else:
        f = request.form["fn"]
        l = request.form["ln"]
        e = request.form["em"]
        p = request.form["pw"]
        data = {'firstname':f, "lastname":1, "email":e, "password":p}
        collection=mongo.db.users
        check = collection.find_one({'email':e})
        if check is None:
            collection.insert(data)
            flash("Account Successfully Registered")
            return redirect('/login')
        else:
            flash("Email already registered")
            return redirect('/')


@a.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        e = request.form["em"]
        p = request.form["pw"]
        collection = mongo.db.users
        user = collection.find_one({'email':e, 'password':p})
        if user is None:
            return redirect("/login")
        else:
            session['active'] = True
            session['user'] = e
            return redirect('/post')


@a.route("/post", methods = ["GET", "POST"])
def post():
    if 'active' in session and session['active'] ==  True:
        if request.method == "GET":
            posts = mongo.db.posts.find().sort('Posted', -1).limit(10)
            return render_template("post.html", posts = posts)
        else:
                p = request.form["post"]
                u = session['user']
                newpost = {"From":u, "Post":p, "Posted":datetime.utcnow()}
                collection = mongo.db.posts
                collection.insert(newpost)
                return redirect('/post')

    else:
        flash("You need to login first to access this page.")
        return redirect("/login")


@a.route("/logout")
def logout():
    session['active'] = False
    flash("Successfully logged out")
    return redirect('/login')


@a.route("/messages", methods = ["GET", "POST"])
def messages():
    if 'active' in session and session['active'] == True:
        if request.method == "GET":
            v = mongo.db.messages.find({'From': session['user']})
            u = mongo.db.messages.find({'To': session['user']})
            return render_template("messages.html", sent = v, received = u)
        else:
            t = request.form['receiver']
            m = request.form['message']
            ti = datetime.utcnow()
            u = session['user']
            newmessage = {'From':u, 'To':t, 'Message':m, 'Time':ti}
            collection = mongo.db.messages
            collection.insert(newmessage)
            flash('Message sent successfully')
            return redirect('/messages')

    else:
        flash("You need to login first to access this page.")
        return redirect("/login")



a.run(debug = True)

