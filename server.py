from jinja2 import StrictUndefined
from flask import (Flask, render_template, request, flash, redirect,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import UploadSet, configure_uploads, IMAGES
from model import (connect_to_db, db, User, Business, UserBiz, CheckIn, Review,
                   LikeReview)
from datetime import datetime
import helper
import re
import constants as c


app = Flask(__name__)

pics = UploadSet('pics', IMAGES)

app.config['UPLOADED_PICS_DEST'] = 'static/img'
configure_uploads(app, pics)

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
    biz = request.form['biz']

    # Convert picture that would be saved to static/img directory but url stored
    # in database
    if 'pic' in request.files:
        filename = pics.save(request.files['pic'])
        pic = pics.url(filename)
    else:
        pic = None

    # TO DELETE
    print u'\n\n\n{}\n\n\n'.format(username)
    print u'\n\n\n{}\n\n\n'.format(biz)

    # Convert birthday to datetime format
    if bday_str:
        bday = datetime.strptime(bday_str, '%Y-%m-%d')
    else:
        bday = None

    # Convert boolean to python format
    if biz == 'true':
        biz = True
    else:
        biz = False

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
                    join_date=datetime.today().date(),
                    biz_acct=biz)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.user_id
        session['username'] = user.username
        session['biz_acct'] = user.biz_acct

        if user.user_pic:
            session['user_pic'] = user.user_pic
        else:
            session['user_pic'] = '/static/img/dragonfly.jpeg'

        flash('{} is now registered and logged in as {}'.format(user.email, user.username))

        return redirect('/')


# @app.route('/login')
# def login_form():
#     """Displays form for user to log-in."""

#     return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login_process():
    """Logs in user."""

    user_input = request.form.get('user-input')
    pword = request.form.get('pword')

    user = helper.check_user_info(user_input)

    if not user:
        code = 'error'
        results = 'User name or email does not exist. Please check your input or register.'
    elif user.password != pword:
        code = 'error'
        results = 'The password is incorrect. Please check you input or reset password.'
    else:
        session['user_id'] = user.user_id
        session['username'] = user.username
        session['biz_acct'] = user.biz_acct

        if user.user_pic:
            session['user_pic'] = user.user_pic
        else:
            session['user_pic'] = '/static/img/dragonfly.jpeg'

        code = 'success'
        results = user.username + ' is now logged in.'

    return jsonify({'code': code, 'msg': results})


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

    user = helper.check_user_info(user_input)

    if not user:
        return False
    else:
        return True
        email = user.email

    # TO DO: need to send link to user email to reset password


# The below is coming from password.html. At the moment, nothing renders the page
# as AJAX refactoring stays on the page with email with password reset link being sent
@app.route('/pword-reset', methods=['POST'])
def reset_pword():
    """Resets user password."""

    user_input = request.form['user']
    new_pword = request.form['pword']

    user = helper.check_user_info(user_input)

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
    print u'\n\n\n{}\n\n\n'.format(user.reviews)
    print u'\n\n\n{}\n\n\n'.format(user.friends)
    print u'\n\n\n{}\n\n\n'.format(user.referees)
    print u'\n\n\n{}\n\n\n'.format(user.promos)

    # friends = helper.calc_friends(user)
    # session['tot_friends'] = friends

    # reviews = helper.calc_reviews(user)
    # session['tot_revs'] = reviews

    # FIXME: update helper function once relationship mapping is solved.
    total_refs, redeemed_refs = helper.calc_referrals(user)
    session['tot_refs'] = total_refs
    session['redeem_refs'] = redeemed_refs

    redemptions = helper.calc_redemptions(user)
    session['tot_redeem'] = redemptions

    # checkins = helper.calc_checkins(user)
    # session['tot_checkins'] = checkins

    # refer_to_user = Referral.query.filter_by(referee_id=session['user_id']).all()

    return render_template('user_profile.html', user=user)


@app.route('/user-friends')
def user_friends():
    """Displays user's friends list with abbreviated profile."""

    user = User.query.filter_by(user_id=session['user_id']).first()

    # TO DELETE
    print u'\n\n\n{}\n\n\n'.format(user.friends)

    return render_template('user_friends.html', user=user)


@app.route('/friend-profile/<int:friend_id>')
def friend_profile(friend_id):
    """Displays friend information."""

    friend = User.query.filter_by(user_id=friend_id).first()

    # TO DELETE
    print u'\n\n\n{}\n\n\n'.format(friend.reviews)
    print u'\n\n\n{}\n\n\n'.format(friend.friends)
    print u'\n\n\n{}\n\n\n'.format(friend.referees)
    print u'\n\n\n{}\n\n\n'.format(friend.promos)

    friends = helper.calc_friends(friend)
    reviews = helper.calc_reviews(friend)
    total_refs, redeemed_refs = helper.calc_referrals(friend)
    redemptions = helper.calc_redemptions(friend)
    checkins = helper.calc_checkins(friend)

    return render_template('friend_profile.html', user=friend,
                           checkins=checkins,
                           reviews=reviews,
                           refs=total_refs,
                           redeem_refs=redeemed_refs,
                           redeem_promos=redemptions,
                           friends=friends)


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

    # Convert picture that would be saved to static/img directory but url stored
    # in database
    if 'pic' in request.files:
        filename = pics.save(request.files['pic'])
        pic = pics.url(filename)
    else:
        pic = None

    # TO DELETE
    print u'\n\n\n{}\n\n\n'.format(name)
    print u'\n\n\n{}\n\n\n'.format(claim)

    # Convert time to military format
    if open_mil == 'pm':
        open_time += 12

    if close_mil == 'pm':
        close_time += 12

    # Convert phone to same format
    re.sub('\ |\?|\.|\!|\/|\;|\:|\-|\(|\)', '', phone)

    # Convert boolean to python format
    if claim == 'true':
        claim = True
    else:
        claim = False

    # Check if business is already in database
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

        db.session.add(biz)
        db.session.commit()

        if claim:
            userbiz = UserBiz(user_id=session['user_id'], biz_id=biz.biz_id)

            db.session.add(userbiz)
            db.session.commit()

        flash('{} has been added'.format(biz.biz_name))

        return redirect('/')


@app.route('/business-profile/<biz_name>')
def biz_profile(biz_name):
    """Displays business information."""

    biz = Business.query.filter_by(biz_name=biz_name).first()
    today = datetime.today()
    category = c.BIZ_CATEGORY.get(biz.category)

    # TO DELETE
    print u'\n\n\n{}\n\n\n'.format(biz_name)
    print u'\n\n\n{}\n\n\n'.format(biz.reviews)
    print u'\n\n\n{}\n\n\n'.format(biz.referrals)
    print u'\n\n\n{}\n\n\n'.format(biz.promos)
    print u'\n\n\n{}\n\n\n'.format(biz.users)

    avg_score, count = helper.calc_avg_rating(biz)
    tot_checkins = helper.calc_biz_tot_checkins(biz)
    user_checkins = helper.calc_checkins_biz(biz.biz_id)
    promos_redeem = helper.calc_biz_promos_redeem(biz)
    total_refs, redeemed_refs = helper.calc_biz_referrals(biz)

    user_review = Review.query.filter(Review.biz_id == biz.biz_id,
                                      Review.user_id == session['user_id']).first()

    if user_review:
        if user_review.revise_review:
            user_rating = user_review.new_rating
        else:
            user_rating = user_review.rating
    else:
        user_rating = 'N/A'

    # TO DELETE
    print u'\n\n\n{}\n\n\n'.format(promos_redeem)

    # TO DO: build out helper functions to pull in totals to summarize;
    # format phone number and hours

#     query using:
# for approximations of nearby distances using spherical distance, search units nearby by meters; example below searches within 1000m
# db.session.query(UnitDetails).filter(func.ST_Distance_Sphere("POINT(37.776164 -122.423355)",UnitDetails.latlng) < 1000).all()

    return render_template('business_profile.html', biz=biz, today=today,
                           category=category, score=avg_score, count=count,
                           checkins=tot_checkins, user_checkins=user_checkins,
                           promos_redeem=promos_redeem, refs=total_refs,
                           ref_redeem=redeemed_refs, user_score=user_rating)


@app.route('/checkin/<int:biz_id>', methods=['POST'])
def check_in(biz_id):
    """Checks in user into business, limit one check in per day. """

    today = datetime.today().date()
    checkin = (CheckIn.query.filter(CheckIn.user_id == session['user_id'],
               CheckIn.biz_id == biz_id, CheckIn.checkin_date == today).first())
    biz = Business.query.get(biz_id)
    biz_name = biz.biz_name

    # TO DELETE
    print u'\n\n\n{}\n\n\n'.format(biz.biz_name)

    if checkin:
        flash('You have already checked into this business today. No double dipping!')
    else:
        checkin = CheckIn(user_id=session['user_id'],
                          biz_id=biz_id,
                          checkin_date=today)

        db.session.add(checkin)
        db.session.commit()

        user_checkins = helper.calc_checkins_biz(biz_id)

        flash('You have checked in a total of {} times. {} thanks you for your support!'.format(user_checkins, biz.biz_name))

    # TO DELETE
    print u'\n\n\n{}\n\n\n'.format(biz_name)
    import pdb; pdb.set_trace()

    # return redirect('/')

    return redirect('/business-profile/<biz_name>')

    # FIXME: redirect isn't taking in biz_name


@app.route('/review/<biz_name>')
def review_form(biz_name):
    """Displays form to review a business."""

    return render_template('review_form.html', biz_name=biz_name)


@app.route('/review/<biz_name>', methods=['POST'])
def review_process(biz_name):
    """Processes user review of business."""

    score = request.form['rating']
    comment = request.form['review']
    today = datetime.today().date()
    biz = Business.query.filter_by(biz_name=biz_name).first()

    review = Review(user_id=session['user_id'],
                    biz_id=biz.biz_id,
                    rating=int(score),
                    review=comment,
                    review_date=today)

    db.session.add(review)
    db.session.commit()

    flash('Your review has been received. {} appreciates your feedback.'.format(biz_name))

    return redirect('/business-profile/<biz_name>')


@app.route('/like-review', methods=['POST'])
def like_process():
    """Processes user's like of specific review."""

    review_id = request.form['review_id']

    like = LikeReview(review_id=review_id, user_id=session['user_id'])

    db.session.add(like)
    db.session.commit()

    return 'Thanks for liking me!'


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
