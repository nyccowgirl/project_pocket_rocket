from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, request, flash, redirect,
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User  # Business

from datetime import datetime

import buddy


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SHHHHHHIIIITTTT"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Displays homepage."""

    return render_template('home.html')


@app.route('/register')
def register_form():
    """Displays form for user registration/sign up."""

    return render_template('registration_form.html')


@app.route('/register', methods=['POST'])
def register_process():
    """Processes registration form."""

    # Get form variables
    fname = request.form['fname']
    lname = request.form['lname']
    username = request.form['username']
    email = request.form['email']
    pword = request.form['pword']
    bday_str = request.form['bday']
    # pic = request.form['pic']
    biz = request.form['biz']

    # TO DELETE
    print '\n\n\n{}\n\n\n'.format(username)
    print '\n\n\n{}\n\n\n'.format(biz)

    # Convert birthday to datetime format
    if bday_str:
        bday = datetime.strptime(bday_str, '%Y-%m-%d')
    else:
        bday = None

    # Check if user is already in database
    user = User.query.filter_by(email=email).first()

    if user:
        flash('The email provided already has an account. Please log-in.')
        return redirect('/login')
    else:
        user = User(username=username,
                    first_name=fname,
                    last_name=lname,
                    email=email,
                    password=pword,
                    # user_pic=pic,
                    dob=bday,
                    join_date=datetime.now(),
                    biz_acct=biz)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.user_id
        session['username'] = user.username
        flash('{} is now registered and logged in as {}'.format(user.email, user.username))

        return redirect('/')


@app.route('/login')
def login_form():
    """Displays form for user to log-in."""

    return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login_process():
    """Logs in user."""

    user_input = request.form['user']
    pword = request.form['pword']

    user = buddy.check_user_info(user_input)
    # TO DO: move this to AJAX(?) to check it in html first, where if email/username
    # does not exist, then note error for user to re-input; otherwise, go to registration

    if not user:
        flash('User name or email does not exist. Please check your input or register.')
        return redirect('/login')
    elif user.password != pword:
        flash('The password is incorrect. Please check you input or reset password.')
        return redirect('/login')
    else:
        session['user_id'] = user.user_id
        session['username'] = user.username
        flash('{} is now logged in.'.format(user.username))

        return redirect('/')


@app.route('/logout')
def logout():
    """Logs out user."""

    session.clear()

    flash('Thanks for being a BUDdy. Continue to be your badass self and have a fantabulous day!')

    return redirect('/')


@app.route('/pword-reset')
def check_email():
    """Checks user info in database when user wants to reset password."""

    user_input = request.form['user']

    user = buddy.check_user_info(user_input)

    if not user:
        return False
    else:
        return True

    # TO DO: need to send link to user email to reset password


@app.route('/pword-reset', methods=['POST'])
def reset_pword():
    """Resets user password."""

    user_input = request.form['user']
    new_pword = request.form['pword']

    user = buddy.check_user_info(user_input)

    user.password = new_pword
    db.session.commit()
    session['user_id'] = user.user_id
    session['username'] = user.username

    flash('{} is now logged in.'.format(user.username))

    return redirect('/')


@app.route('/user-profile')
def user_profile():
    """Displays user information."""

    user = User.query.filter_by(user_id=session['user_id']).first()

    # TO DELETE
    print '\n\n\n{}\n\n\n'.format(user.reviews)
    print '\n\n\n{}\n\n\n'.format(user.friends)
    print '\n\n\n{}\n\n\n'.format(user.referrals)
    print '\n\n\n{}\n\n\n'.format(user.promos)

    # TO DO: build out helper functions to pull in totals to summarize

    return render_template('/user_profile.html', user=user)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
