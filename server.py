from jinja2 import StrictUndefined
from flask import (Flask, render_template, request, flash, redirect,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import UploadSet, configure_uploads, IMAGES
from model import (connect_to_db, db, User, Business, UserBiz, CheckIn, Review,
                   LikeReview, Friend, Invite)
from datetime import datetime
import helper
import re
# import constants as c
from sqlalchemy import or_, desc
from bubble import bubble_data_refs, bubble_data_promos
from friend_network import make_nodes_and_paths, see_friends

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

    bubble_data_refs()
    bubble_data_promos()

    return render_template('home.html')


# @app.route('/bubble')
# def bubble():
#     """Displays bubble chart."""

#     return render_template('bubble.html')


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
    # import pdb; pdb.set_trace()
    # Get form variables
    fname = request.form['fname']
    lname = request.form['lname']
    username = request.form['username']
    email = request.form['email-reg']
    pword = request.form['pword-reg']
    bday_str = request.form['bday']
    biz = request.form['biz']

        # TO DELETE
    # print u'\n\n\n{}\n\n\n'.format(fname)
    # print u'\n\n\n{}\n\n\n'.format(lname)
    # print u'\n\n\n{}\n\n\n'.format(username)
    # print u'\n\n\n{}\n\n\n'.format(email)
    # print u'\n\n\n{}\n\n\n'.format(pword)
    # print u'\n\n\n{}\n\n\n'.format(bday_str)
    # print u'\n\n\n{}\n\n\n'.format(biz)

    # Convert picture that would be saved to static/img directory but url stored
    # in database
    if 'user-pic' in request.files:
        filename = pics.save(request.files['user-pic'])
        pic = pics.url(filename)
    else:
        pic = None

    # TO DELETE
    # print u'\n\n\n{}\n\n\n'.format(username)
    # print u'\n\n\n{}\n\n\n'.format(biz)

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
        code = 'error'
        results = 'The user name or email provided already has an account. Please log-in.'
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


        code = 'success'
        results = '{} is now registered and logged in as {}'.format(user.email, user.username)

    return jsonify({'code': code, 'msg': results})

# @app.route('/login')
# def login_form():
#     """Displays form for user to log-in."""

#     return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login_process():
    """Logs in user."""

    user_input = request.form.get('user-input')
    pword = request.form.get('pword')

    # TO DELETE
    # print '\n\n\n{}{}\n\n\n'.format(user_input, pword)

    user = User.query.filter((User.username == user_input) | (User.email == user_input)).first()

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

        # TO DELETE
        # print '\n\n\n{}\n\n\n'.format(user.biz_acct)

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


@app.route('/email-check')
def check_email():
    """Checks user info in database when user wants to reset password."""

    user_input = request.form['user-input']

    user = User.query.filter((User.email == email) | (User.username == username)).first()

    if not user:
        return False
    else:
        return True
        email = user.email

    # TO DO: need to send link to user email to reset password

@app.route('/pword-reset')
def pword_form():
    """ Displays password reset form. """

    return render_template('password.html')
# The below is coming from password.html. At the moment, nothing renders the page
# as AJAX refactoring stays on the page with email with password reset link being sent
@app.route('/pword-reset', methods=['POST'])
def reset_pword():
    """Resets user password."""

    user_input = request.form['user']
    new_pword = request.form['pword']

    user = User.query.filter((User.email == email) | (User.username == username)).first()

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
    # print u'\n\n\n{}\n\n\n'.format(user.reviews)
    # print u'\n\n\n{}\n\n\n'.format(user.friends)
    # print u'\n\n\n{}\n\n\n'.format(user.referees)
    # print u'\n\n\n{}\n\n\n'.format(user.promos)

    # friends = helper.calc_friends(user)
    # session['tot_friends'] = friends

    # reviews = helper.calc_reviews(user)
    # session['tot_revs'] = reviews

    # FIXME: update helper function once relationship mapping is solved.
    # total_refs, redeemed_refs = helper.calc_referrals(user)
    # session['tot_refs'] = total_refs
    # session['redeem_refs'] = redeemed_refs

    # redemptions = helper.calc_redemptions(user)
    # session['tot_redeem'] = redemptions

    # checkins = helper.calc_checkins(user)
    # session['tot_checkins'] = checkins

    # refer_to_user = Referral.query.filter_by(referee_id=session['user_id']).all()

    return render_template('user_profile.html', user=user)


@app.route('/edit-user', methods=['POST'])
def edit_user():
    """Processes edit user request."""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    pword = request.form.get('pword')
    biz_acct = request.form.get('biz_acct')

    user = User.query.filter_by(user_id=session['user_id']).first()

    check_email = User.query.filter_by(email=email).first()

    # Convert picture that would be saved to static/img directory but url stored
    # in database
    if 'pic' in request.files:
        filename = pics.save(request.files['pic'])
        pic = pics.url(filename)
    else:
        pic = None

    if check_email:
        code = 'error'
        results = 'That email is already used.'
    elif (user.biz_acct is True) and (biz_acct == 'false'):
        code = 'warning'
        results = 'This account currently has business(es) claimed to it. Do you want to unclaim?'
        # FIXME: Move to AJAX for email check and biz confirmation using jQuery AJAX .change() event handler.
    else:
        if fname:
            user.first_name = fname

        if lname:
            user.last_name = lname

        if email:
            user.email = email

        if pword:
            user.password = pword

        if pic:
            user.user_pic = pic

        if biz_acct:
            if biz_acct == 'true':
                user.biz_acct = True
            else:
                user.biz_acct = False

        db.session.commit()

        code = 'success'
        results = 'Your user information has been updated.'

        return jsonify({'code': code, 'msg': results})


@app.route('/user-friends')
def user_friends():
    """Displays user's friends list with abbreviated profile."""

    user = User.query.filter_by(user_id=session['user_id']).first()

    # TO DELETE
    # print u'\n\n\n{}\n\n\n'.format(user.friends)

    # print u'\n\n\n{}\n\n\n'.format(user.friends[0].tot_biz_referrals)

    return render_template('user_friends.html', user=user)


@app.route('/add-friend', methods=['POST'])
def add_friend():
    """Processes add friend request."""

    friend_email = request.form.get('friend-email')

    # TO DELETE
    # print u'\n\n\n{}\n\n\n'.format(friend_email)
    # print request.form.get('friend-email')
    # print request.form.get('friend_email')

    friend = User.query.filter_by(email=friend_email).first()

    if not friend:
        # TO DO: Use third party API like MailChimp/Mandrill to generate registration
        # friend request email

        invite = Invite(user_id=session['user_id'], friend_email=friend_email)

        db.session.add(invite)
        db.session.commit()

        results = 'A request has been sent to ' + friend_email
    else:
        # Checks if already existing friends
        am_friend = Friend.query.filter(user_id=session['user_id'],
                                        friend_id=friend.user_id).first()
        is_friend = Friend.query.filter(user_id=friend.user_id,
                                        friend_id=session['user_id']).first()

        if am_friend or is_friend:
            results = 'You are already friends with ' + friend.username
        else:
            friend = Friend(user_id=session['user_id'],
                            friend_id=friend.user_id)

            friend_rev = Friend(user_id=friend.user_id,
                                friend_id=session['user_id'])

            db.session.add(friend, friend_rev)
            db.session.commit()

            results = friend.username + "is now your friend."

    print results

    return jsonify(results)


@app.route('/user-reviews')
def user_reviews():
    """Displays user's reviews with abbreviated profile."""

    user = User.query.filter_by(user_id=session['user_id']).first()

    # TO DELETE
    # print u'\n\n\n{}\n\n\n'.format(user.reviews)

    return render_template('user_reviews.html', user=user)


@app.route('/reviews-home')
def display_biz_reviews():
    """Displays search feature to find business to review and businesses recently
    checked into that have not been reviewed."""

    checkins = CheckIn.query.filter_by(user_id=session['user_id']).all()

    return render_template('reviews_home.html', checkins=checkins)


@app.route('/friend-profile/<int:friend_id>')
def friend_profile(friend_id):
    """Displays friend information."""

    friend = User.query.filter_by(user_id=friend_id).first()

    # TO DELETE
    # print u'\n\n\n{}\n\n\n'.format(friend)
    # print u'\n\n\n{}\n\n\n'.format(friend.reviews)
    # print u'\n\n\n{}\n\n\n'.format(friend.friends)
    # print u'\n\n\n{}\n\n\n'.format(friend.referees)
    # print u'\n\n\n{}\n\n\n'.format(friend.promos)

    # friends = helper.calc_friends(friend)
    # reviews = helper.calc_reviews(friend)
    # total_refs, redeemed_refs = helper.calc_referrals(friend)
    # redemptions = helper.calc_redemptions(friend)
    # checkins = helper.calc_checkins(friend)

    return render_template('friend_profile.html', friend=friend)


@app.route('/user-promos')
def user_promos():
    """Displays user's available promotions and redemptions."""

    user = User.query.filter_by(user_id=session['user_id']).first()

    # TO DELETE
    # print u'\n\n\n{}\n\n\n'.format(user.promos)

    # print u'\n\n\n{}\n\n\n'.format(user.friends[0].tot_biz_referrals)

    return render_template('user_promos.html', user=user)


@app.route('/user-referrals')
def user_referrals():
    """Displays user's referrals and related redemptions."""

    user = User.query.filter_by(user_id=session['user_id']).first()

    # TO DELETE
    # print u'\n\n\n{}\n\n\n'.format(user.referrals)

    # print u'\n\n\n{}\n\n\n'.format(user.friends[0].tot_biz_referrals)

    return render_template('user_referrals.html', user=user)


@app.route('/user-biz')
def user_biz():
    """Displays user's businesses and related analytics."""

    user = User.query.filter_by(user_id=session['user_id']).first()

    # TO DELETE
    # print u'\n\n\n{}\n\n\n'.format(user.biz)

    # print u'\n\n\n{}\n\n\n'.format(user.friends[0].tot_biz_referrals)

    return render_template('user_biz.html', user=user)


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
    # print u'\n\n\n{}\n\n\n'.format(name)
    # print u'\n\n\n{}\n\n\n'.format(claim)

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
    # category = c.BIZ_CATEGORY.get(biz.category)

    # # TO DELETE
    # print u'\n\n\n{}\n\n\n'.format(biz_name)
    # print u'\n\n\n{}\n\n\n'.format(biz.reviews)
    # print u'\n\n\n{}\n\n\n'.format(biz.referrals)
    # print u'\n\n\n{}\n\n\n'.format(biz.promos)
    # print u'\n\n\n{}\n\n\n'.format(biz.users)

    # avg_score, count = helper.calc_avg_rating(biz)
    # tot_checkins = helper.calc_biz_tot_checkins(biz)
    # user_checkins = helper.calc_checkins_biz(biz.biz_id)
    # promos_redeem = helper.calc_biz_promos_redeem(biz)
    # total_refs, redeemed_refs = helper.calc_biz_referrals(biz)

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
    # print u'\n\n\n{}\n\n\n'.format(promos_redeem)

    # TO DO: build out helper functions to pull in totals to summarize;
    # format phone number and hours

#     query using:
# for approximations of nearby distances using spherical distance, search units nearby by meters; example below searches within 1000m
# db.session.query(UnitDetails).filter(func.ST_Distance_Sphere("POINT(37.776164 -122.423355)",UnitDetails.latlng) < 1000).all()

    return render_template('business_profile.html', biz=biz, today=today,
                           user_score=user_rating)


@app.route('/claim-biz/<int:biz_id>', methods=['POST'])
def claim_biz(biz_id):
    """Processes user claiming ownership of a business."""

    check = UserBiz.query.filter_by(biz_id=biz_id).first()

    if check:
        code = 'error'
        results = 'The business has already been claimed. If you believe this is in \
              error, please submit message to administrators and provide evidence of your ownership.'
    else:
        userbiz = UserBiz(user_id=session['user_id'],
                          biz_id=biz_id)

        db.session.add(userbiz)
        db.session.commit()
        code = 'success'
        results = 'Thanks for being part of the BUDdy community.'

    return jsonify({'code': code, 'msg': results})


@app.route('/checkin/<int:biz_id>', methods=['POST'])
def check_in(biz_id):
    """Checks in user into business, limit one check in per day. """

    today = datetime.today().date()
    checkin = (CheckIn.query.filter(CheckIn.user_id == session['user_id'],
               CheckIn.biz_id == biz_id, CheckIn.checkin_date == today).first())
    biz = Business.query.get(biz_id)
    biz_name = biz.biz_name

    # TO DELETE
    # print u'\n\n\n{}\n\n\n'.format(biz.biz_name)

    if checkin:
        results = 'You have already checked into this business today. No double dipping!'
    else:
        checkin = CheckIn(user_id=session['user_id'],
                          biz_id=biz_id,
                          checkin_date=today)

        db.session.add(checkin)
        db.session.commit()

        user_checkins = helper.calc_checkins_biz(biz_id)

        results = ('You have checked in a total of {} times. {} thanks you for your support!'.format(user_checkins, biz_name))

    # TO DELETE
    # print u'\n\n\n{}\n\n\n'.format(biz_name)
    # import pdb; pdb.set_trace()

    # return redirect('/'))

    return jsonify(results)

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


@app.route('/search-biz')
def search():
    """Searches business table based on user provided keywords."""

    # TO DO: Convert to full text searchability via https://sqlalchemy-searchable.readthedocs.io/en/latest/index.html

    keywords = '%' + request.args.get('search') + '%'

    search = Business.query.filter(or_(Business.biz_name.ilike(keywords),
                                       Business.category.ilike(keywords))).all()

    return render_template('search_results.html', search=search)


@app.route('/review-home')
def review_home():
    """Displays review home page with list of businesses that have been checked into
    but not reviewed by user, limited to most recent 10."""

    # user = User.query.filter_by(user_id=session['user_id']).first()

    recent_checkins = CheckIn.query.filter_by(user_id=session['user_id']).order_by(desc(CheckIn.checkin_date)).group_by(CheckIn.checkin_id, CheckIn.biz_id).limit(10).all()

    return render_template('reviews_home.html', checkins=recent_checkins)


@app.route('/data.json')
def get_graph_data_default():
    """ Create nodes and paths from friends table and jsonify for force layout."""

    degree = request.args.get('degree')

    if degree:
        nodes, paths = make_nodes_and_paths(see_friends(session['user_id'], int(degree)))
    else:
        nodes, paths = make_nodes_and_paths(see_friends(session['user_id'], 2))

    return jsonify({'nodes': nodes, 'paths': paths})


# @app.route('/data.json', methods=['POST'])
# def get_graph_data():
#     """ Create nodes and paths from friends table and jsonify for force layout."""

#     degree = request.form.get('degree')
#     print degree

#     if degree:
#         nodes, paths = make_nodes_and_paths(see_friends(session['user_id'], int(degree)))

#     # import pdb; pdb.set_trace()
#     print nodes
#     return jsonify({'nodes': nodes, 'paths': paths})


# @app.route('/network')
# def index_advanced():
#     """Return homepage."""

#     return render_template('friend_network.html')

@app.route('/respond/<int:review_id>')
def response_form(review_id):
    """ Displays response form to a specific user review for business. """

    review = Review.query.filter_by(review_id=review_id).first()

    return render_template('response_form.html', review=review)


@app.route('/respond/<int:review_id>', methods=['POST'])
def rev_resp_process(review_id):

    response = request.form.get('ref-response')

    rev_resp = Review(dispute=True, response=response)

    db.session.add(rev_resp)
    db.session.commit()

    flash("Your response has been posted. Thanks for addressing the reviewer's comments.")

    return redirect('/user-biz')


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
