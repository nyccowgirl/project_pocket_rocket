
from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Business

from datetime import datetime


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SHHHHHHIIIITTTT"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('home.html')


@app.route('/register')
def register_form():
    """Display form for user registration/sign up."""

    return render_template('registration_form.html')


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration form."""

    # Get form variables
    fname = request.form['fname']
    lname = request.form['lname']
    user = request.form['user']
    email = request.form['email']
    pword = request.form['pword']
    bday_str = request.form['bday']
    pic = request.form['pic']
    biz = request.form['biz']

    # Convert birthday to datetime format
    if bday_str:
        bday = datetime.strpime(bday_str, '%Y-%m-%d')
    else:
        bday = None

    # Check if user is already in database
    user = User

    user = User(username=user,
                first_name=fname,
                last_name=lname,
                email=email)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
