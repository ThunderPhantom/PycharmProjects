from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

app = Flask(__name__)

@app.route('/')
def home():
    user = request.args.get('user')
    print('user=',user)
    users = [
    {'name': 'Anne'},
    {'name': 'Bob'},
    {'name':'Anish'},
    {'name':user}
    ]

    return render_template('base.html',name='YoungWonks', users = users)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':

        # renders login page
        return render_template('login.html')
    elif request.method == 'POST':
        user = request.form.get('user')
        # redirects to home page if login is successful

        return redirect(url_for('home', user=user))



if __name__ == '__main__':
    app.run(debug = True)
