from flask import Flask, session

from model import connect_to_db, User, CheckIn  # db, Business

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SHHHHHHIIIITTTT"

##############################################################################


def check_user_info(user_input):
    """
    Checks user input of either username or email against database.

    >>> check_user_info('123@abc.com')

    >>>> check_user_info('hello@hello.com')
    <user_id=...>
    """

    user = User.query.filter((User.username == user_input) | (User.email == user_input)).first()

    return user


def calc_checkins(user_obj):
    """
    Calculates total check-ins for gamification component.

    TO DO: Build out doctests
    """

    total = user_obj.checkins.count()

    return total


def calc_reviews(user_obj):
    """
    Calculates total reviews for gamification component.

    TO DO: Build out doctests
    """

    total = user_obj.reviews.count()

    return total


def calc_referrals(user_obj):
    """
    Calculates total referrals for gamification component.

    TO DO: Build out doctests
    """

    total_refs = user_obj.referees.count()
    redeemed_refs = 0

    for item in user_obj.referees:
        if item.user_promos.redeemed is True:
            redeemed_refs += 1

    return total_refs, redeemed_refs


def calc_checkins_biz(biz_id):
    """
    Calculates total check-ins per business for gamification component.

    TO DO: Build out doctests
    """

    total = CheckIn.query.filter(CheckIn.user_id == session['user_id'], CheckIn.biz_id == biz_id).count()

    return total

##############################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)