from jinja2 import StrictUndefined

from flask import (Flask, render_template, request, flash, redirect,
                   session)  # jsonify

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Business, UserBiz, CheckIn

from datetime import datetime

import buddy

import re


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SHHHHHHIIIITTTT"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.template_filter()
def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    """Custom Jinja filter to format dates consistently."""

    return value.strftime(format)


##############################################################################

@app.route('/')
def index():
    """Displays homepage."""

    return render_template('home.html')


@app.route('/about-us')
def about():
    """Displays about us page."""

    return render_template('about.html')


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
    pic = request.form['pic']
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
    user = User.query.filter((User.email == email) | (User.username == username)).first()

    if user:
        flash('The user name or email provided already has an account. Please log-in.')
        return redirect('/login')
    else:
        user = User(username=username,
                    first_name=fname,
                    last_name=lname,
                    email=email,
                    password=pword,
                    user_pic=pic,
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

    user_input = request.form['user-info']
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
    print '\n\n\n{}\n\n\n'.format(user.referees)
    print '\n\n\n{}\n\n\n'.format(user.promos)

    # TO DO: build out helper functions to pull in totals to summarize

    return render_template('/user_profile.html', user=user)


@app.route('/friend-profile/<int:friend_id>')
def friend_profile(friend_id):
    """Displays friend information."""

    friend = User.query.filter_by(user_id=friend_id).first()

    # TO DELETE
    print '\n\n\n{}\n\n\n'.format(friend.reviews)
    print '\n\n\n{}\n\n\n'.format(friend.friends)
    print '\n\n\n{}\n\n\n'.format(friend.referees)
    print '\n\n\n{}\n\n\n'.format(friend.promos)

    # TO DO: build out helper functions to pull in totals to summarize

    return render_template('/friend_profile.html', user=friend)


@app.route('/add-biz')
def biz_form():
    """Displays form to add a business."""

    return render_template('business_form.html')


@app.route('/add-biz', methods=['POST'])
def biz_process():
    """Processes new business request."""

    # Get form variables
    name = request.form['name']
    address = request.form['addy']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    zipcode = request.form['zipcode']
    phone = request.form['tel']
    email = request.form['email']
    url = request.form['url']
    category = request.form['category']
    days_open = request.form['days-open']
    open_time = int(request.form['time-open'])
    open_mil = request.form['open-ampm']
    close_time = int(request.form['time-close'])
    close_mil = request.form['close-ampm']
    claim = request.form['claim']
    pic = request.form['pic']

    # TO DELETE
    print '\n\n\n{}\n\n\n'.format(name)
    print '\n\n\n{}\n\n\n'.format(claim)

    # Convert time to military format
    if open_mil == 'pm':
        open_time += 12

    if close_mil == 'pm':
        close_time += 12

    # Convert phone to same format
    re.sub('\ |\?|\.|\!|\/|\;|\:|\-|\(|\)', '', phone)

    # Check if user is already in database
    business = Business.query.filter((Business.email == email) | (Business.biz_name == name)).first()

    if business:
        flash('The business name or email provided is already in BUDdy.')
        return redirect('/login')
    else:
        biz = Business(biz_name=name,
                       address=address,
                       city=city,
                       state=state,
                       country=country,
                       zipcode=zipcode,
                       phone=phone,
                       email=email,
                       url=url,
                       category=category,
                       days_open=days_open,
                       open_time=open_time,
                       close_time=close_time,
                       claimed=claim,
                       biz_pic=pic)

        # TO DELETE
        print '\n\n\n{}\n\n\n'.format(claim)

        if claim:
            userbiz = UserBiz(user_id=session['user_id'], biz_id=biz.biz_id)

        db.session.add(biz, userbiz)
        db.session.commit()

        flash('{} has been added'.format(biz.biz_name))

        return redirect('/')


@app.route('/business-profile/<biz_name>')
def biz_profile(biz_name):
    """Displays business information."""

    biz = Business.query.filter_by(biz_name=biz_name).first()
    today = datetime.today()

    # TO DELETE
    print '\n\n\n{}\n\n\n'.format(biz_name)
    print '\n\n\n{}\n\n\n'.format(biz.reviews)
    print '\n\n\n{}\n\n\n'.format(biz.referrals)
    print '\n\n\n{}\n\n\n'.format(biz.promos)
    print '\n\n\n{}\n\n\n'.format(biz.users)

    # TO DO: build out helper functions to pull in totals to summarize;
    # format phone number and hours

    return render_template('/business_profile.html', biz=biz, today=today)


@app.route('/checkin/<int:biz_id>', methods=['POST'])
def check_in(biz_id):
    """Checks in user into business, limit one check in per day. """

    today = datetime.today()
    checkin = (CheckIn.query.filter(CheckIn.user_id == session['user_id'],
               CheckIn.biz_id == biz_id, CheckIn.checkin_date == today).first())
    biz = Business.query.get(biz_id)

    # TO DELETE
    print '\n\n\n{}\n\n\n'.format(biz.biz_name)

    if checkin:
        flash('You have already checked into this business today. No double dipping!')
    else:
        checkin = CheckIn(user_id=session['user_id'],
                          biz_id=biz_id,
                          checkin_date=today)

        db.session.add(checkin)
        db.session.commit()

        total_checkins = buddy.calc_checkins_biz(biz_id)

        flash('You have checked in a total of {} times. {} thanks you for your support!'.format(total_checkins, biz.biz_name))

    session['checkin'].append(biz.biz_name)

    # TO DELETE
    print '\n\n\n{}\n\n\n'.format(biz.biz_name)
    print '\n\n\n{}\n\n\n'.format(session['checkin'])

    return redirect('/business-profile/<biz.biz_name>')


##############################################################################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
