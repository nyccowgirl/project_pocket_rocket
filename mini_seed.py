"""Utility file to seed buddy database from mini files for testing"""

from sqlalchemy import func
from model import (User, Business, Friend, UserPromo, UserBiz, Review, Referral,
                   Promo, CheckIn, LikeReview, Invite, connect_to_db, db)

from datetime import datetime

from server import app


def load_users():
    """Load users from mini_user into database."""

    print 'Users'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read user file and insert data
    for i, row in enumerate(open('data/mini_user.csv', 'rU')):
        row = row.rstrip()

        user_id, username, first_name, last_name, email, valid_email, password, dob_str, join_date_str, biz_acct = row.split(',')

        dob = datetime.strptime(dob_str, '%m/%d/%y')
        join_date = datetime.strptime(join_date_str, '%m/%d/%y')

        user = User(user_id=user_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    valid_email=valid_email,
                    password=password,
                    dob=dob,
                    join_date=join_date,
                    biz_acct=biz_acct)

        # Add each user to the session
        db.session.add(user)

    # Commit at end
    db.session.commit()


def load_friends():
    """Load friends relationship from mini_friend into database."""

    print 'Friends'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Friend.query.delete()

    # Read user file and insert data
    for i, row in enumerate(open('data/mini_friend.csv', 'rU')):
        row = row.rstrip()

        link_id, user_id, friend_id = row.split(',')

        friend = Friend(link_id=link_id,
                        user_id=int(user_id),
                        friend_id=int(friend_id))

        # Add each friend relationship to the session
        db.session.add(friend)

    # Commit at end
    db.session.commit()


def load_userbiz():
    """Load user-biz relationship from mini_userbiz into database."""

    print 'UserBiz'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    UserBiz.query.delete()

    # Read user file and insert data
    for i, row in enumerate(open('data/mini_userbiz.csv', 'rU')):
        row = row.rstrip()

        userbiz_id, user_id, biz_id = row.split(',')

        userbiz = UserBiz(userbiz_id=userbiz_id,
                          user_id=int(user_id),
                          biz_id=int(biz_id))

        # Add each user-biz relationship to the session
        db.session.add(userbiz)

    # Commit at end
    db.session.commit()


def load_biz():
    """Load businesses from mini_biz into database."""

    print 'Business'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Business.query.delete()

    # Read user file and insert data
    for i, row in enumerate(open('data/mini_biz.csv', 'rU')):
        row = row.rstrip()

        biz_id, biz_name, address, city, state, country, zipcode, email, valid_email, phone, days_open, open_time, close_time, claimed = row.split(',')

        biz = Business(biz_id=biz_id,
                       biz_name=biz_name,
                       address=address,
                       city=city,
                       state=state,
                       country=country,
                       zipcode=zipcode,
                       email=email,
                       valid_email=valid_email,
                       phone=phone,
                       days_open=days_open,
                       open_time=int(open_time),
                       close_time=int(close_time),
                       claimed=claimed)

        # Add each business to the session
        db.session.add(biz)

    # Commit at end
    db.session.commit()


def load_promos():
    """Load promos from mini_promo into database."""

    print 'Promos'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Promo.query.delete()

    # Read user file and insert data
    for i, row in enumerate(open('data/mini_promo.csv', 'rU')):
        row = row.rstrip()

        promo_id, biz_id, title, descr, start_date_str, end_date_str, referral_promo, birthday_promo, redeem_count = row.split(',')

        start_date = datetime.strptime(start_date_str, '%m/%d/%y')
        end_date = datetime.strptime(end_date_str, '%m/%d/%y')

        promo = Promo(promo_id=promo_id,
                      biz_id=int(biz_id),
                      title=title,
                      descr=descr,
                      start_date=start_date,
                      end_date=end_date,
                      referral_promo=referral_promo,
                      birthday_promo=birthday_promo,
                      redeem_count=int(redeem_count))

        # Add each promo to the session
        db.session.add(promo)

    # Commit at end
    db.session.commit()


def load_userpromos():
    """Load user-promos relationship from mini_userpromo into database."""

    print 'UserPromos'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    UserPromo.query.delete()

    # Read user file and insert data
    for i, row in enumerate(open('data/mini_userpromo.csv', 'rU')):
        row = row.rstrip()

        userpromo_id, user_id, promo_id, redeem_date_str, redeemed = row.split(',')

        if redeem_date_str:
            redeem_date = datetime.strptime(redeem_date_str, '%m/%d/%y')

        userpromo = UserPromo(userpromo_id=userpromo_id,
                              user_id=int(user_id),
                              promo_id=int(promo_id),
                              redeem_date=redeem_date,
                              redeemed=redeemed)

        # Add each user-promo relationship to the session
        db.session.add(userpromo)

    # Commit at end
    db.session.commit()


def load_checkin():
    """Load check-ins from mini_checkin into database."""

    print 'CheckIns'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    CheckIn.query.delete()

    # Read user file and insert data
    for i, row in enumerate(open('data/mini_checkin.csv', 'rU')):
        row = row.rstrip()

        checkin_id, user_id, biz_id, checkin_date_str = row.split(',')

        checkin_date = datetime.strptime(checkin_date_str, '%m/%d/%y')

        checkin = CheckIn(checkin_id=checkin_id,
                          user_id=int(user_id),
                          biz_id=int(biz_id),
                          checkin_date=checkin_date)

        # Add each check-in to the session
        db.session.add(checkin)

    # Commit at end
    db.session.commit()


def load_referrals():
    """Load referrals from mini_referrals into database."""

    print 'Referrals'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Referral.query.delete()

    # Read user file and insert data
    for i, row in enumerate(open('data/mini_referral.csv', 'rU')):
        row = row.rstrip()

        referral_id, referer_id, referee_id, biz_id, refer_date_str, userpromo_id = row.split(',')

        refer_date = datetime.strptime(refer_date_str, '%m/%d/%y')

        referral = Referral(referral_id=referral_id,
                            referer_id=int(referer_id),
                            referee_id=int(referee_id),
                            biz_id=int(biz_id),
                            refer_date=refer_date,
                            userpromo_id=int(userpromo_id))

        # Add each referral to the session
        db.session.add(referral)

    # Commit at end
    db.session.commit()


def load_reviews():
    """Load reviews from mini_reviews into database."""

    print 'Reviews'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Review.query.delete()

    # Read user file and insert data
    for i, row in enumerate(open('data/mini_review.csv', 'rU')):
        row = row.rstrip()

        review_id, user_id, biz_id, rating, review, review_date_str, dispute, response, revise_review, new_rating, new_review, cust_svc = row.split(',')

        review_date = datetime.strptime(review_date_str, '%m/%d/%y')

        if new_rating:
            new_rating = int(new_rating)
        else:
            new_rating = None

        if cust_svc:
            cust_svc = int(cust_svc)
        else:
            cust_svc = None

        review = Review(review_id=review_id,
                        user_id=int(user_id),
                        biz_id=int(biz_id),
                        rating=int(rating),
                        review=review,
                        review_date=review_date,
                        dispute=dispute,
                        response=response,
                        revise_review=revise_review,
                        new_rating=new_rating,
                        new_review=new_review,
                        cust_svc=cust_svc)

        # Add each review to the session
        db.session.add(review)

    # Commit at end
    db.session.commit()


def load_likes():
    """Load likes for reviews from mini_likereview into database."""

    print 'LikeReview'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    LikeReview.query.delete()

    # Read user file and insert data
    for i, row in enumerate(open('data/mini_like.csv', 'rU')):
        row = row.rstrip()

        like_id, review_id, user_id = row.split(',')

        like = LikeReview(like_id=like_id,
                          review_id=int(review_id),
                          user_id=int(user_id))

        # Add each like per review to the session
        db.session.add(like)

    # Commit at end
    db.session.commit()


def load_invite():
    """Load invites from mini_invite into database."""

    print 'Invites'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Invite.query.delete()

    # Read user file and insert data
    for i, row in enumerate(open('data/mini_invite.csv', 'rU')):
        row = row.rstrip()

        invite_id, user_id, friend_email, accepted = row.split(',')

        invite = Invite(invite_id=invite_id,
                        user_id=int(user_id),
                        friend_email=friend_email,
                        accepted=accepted)

        # Add each invite to the session
        db.session.add(invite)

    # Commit at end
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_friends()
    load_biz()
    load_userbiz()
    load_promos()
    load_userpromos()
    load_checkin()
    load_referrals()
    load_reviews()
    load_likes()
    load_invite()
    set_val_user_id()
