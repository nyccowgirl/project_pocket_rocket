from __future__ import division
from flask import Flask, session
from model import connect_to_db, User, CheckIn, Promo  # db
from sqlalchemy.sql import extract

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SHHHHHHIIIITTTT"

##############################################################################


def check_user_info(user_input):
    """
    Checks user input of either username or email against database.

    >>> check_user_info('123@abc.com')

    >>> check_user_info('hunk')
    <user_id=...>
    """

    user = User.query.filter((User.username == user_input) | (User.email == user_input)).first()

    return user


# def calc_friends(user_obj):
#     """
#     Calculates total friends for gamification component.

#     TO DO: Build out doctests
#     """

#     total = len(user_obj.friends)

#     return total


# def calc_checkins(user_obj):
#     """
#     Calculates total check-ins for gamification component.

#     TO DO: Build out doctests
#     """

#     total = len(user_obj.checkins)

#     return total


# def calc_reviews(user_obj):
#     """
#     Calculates total reviews for gamification component.

#     TO DO: Build out doctests
#     """

#     total = len(user_obj.reviews)

#     return total


def calc_referrals(user_obj):
    """
    Calculates total referrals and referrals that have been redeemed for
    gamification component.

    >>> calc_referrals(user_obj)
    (6, 11)
    """

    referrals = user_obj.referrals
    total_refs = len(referrals)
    redeemed_refs = 0

    for referral in referrals:
        if referral.user_promo.redeemed is True:
            redeemed_refs += 1

    return total_refs, redeemed_refs


def calc_redemptions(user_obj):
    """
    Calculates total promotions redeemed for gamification component.

    TO DO: Build out doctests
    """

    redeemed_promos = 0

    for promo in user_obj.user_promos:
        if promo.redeemed is True:
            redeemed_promos += 1

    return redeemed_promos


def calc_checkins_biz(biz_id):
    """
    Calculates total check-ins per business for gamification component.

    TO DO: Build out doctests
    """

    total = CheckIn.query.filter(CheckIn.user_id == session['user_id'],
                                 CheckIn.biz_id == biz_id).count()

    return total


def calc_biz_tot_checkins(biz_obj):
    """
    Calculates total check-ins for the business.

    TO DO: Build out doctests
    """

    total_checkins = len(biz_obj.checkins)

    return total_checkins


def calc_biz_promos_redeem(biz_obj):
    """
    Calculates total promotions redeemed by consumers.

    TO DO: Build out doctests
    """

    redeemed_promos = 0

    for promo in biz_obj.promos:
        for item in promo.user_promos:
            if item.redeemed is True:
                redeemed_promos += 1

    return redeemed_promos


def calc_biz_referrals(biz_obj):
    """
    Calculates total referrals and referrals that have been redeemed.

    TO DO: Build out doctests
    """

    total_refs = len(biz_obj.referrals)
    redeemed_refs = 0

    for item in biz_obj.referrals:
        if item.user_promo.redeemed is True:
            redeemed_refs += 1

    return total_refs, redeemed_refs


def calc_avg_rating(biz_obj):
    """
    Calculates average rating per business.

    TO DO: Build out doctests
    """

    reviews = biz_obj.reviews

    count = len(reviews)
    tot_score = 0

    for review in reviews:
        if review.revise_review:
            tot_score += review.new_rating
        else:
            tot_score += review.rating

    avg_rating = tot_score / count

    return avg_rating, count


##############################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)
