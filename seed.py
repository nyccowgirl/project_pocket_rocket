"""Utility file to seed buddy database from mini files for testing"""

from sqlalchemy import func
from model import (User, Business, Friend, UserPromo, UserBiz, Review, Referral,
                   Redemption, Promo, CheckIn, LikeReview, Invite, connect_to_db, db)

from datetime import datetime

from server import app


def load_users():
    """Load users from mini_user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read user file and insert data
    for row in open('data/mini_user'):
        row = row.rstrip()

        user_id, username, first_name, last_name, email, valid_email, password, dob_str, join_date_str, biz_acct = row.split('\t')

        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        join_date = datetime.strptime(join_date_str, '%Y-%m-%d')

        user = User(username=username,
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
    """Load friends relationship from mini_user into database."""

    print "Friends"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Friend.query.delete()

    # Read user file and insert data
    for row in open('data/mini_friend'):
        row = row.rstrip()

        link_id, user_id, friend_id = row.split('\t')

        friend = Friend(user_id=int(user_id), friend_id=int(friend_id))

        # Add each friend relationship to the session
        db.session.add(friend)

    # Commit at end
    db.session.commit()


def load_userbiz():
    """Load user-biz relationship from mini_user into database."""

    print "UserBiz"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    UserBiz.query.delete()

    # Read user file and insert data
    for row in open('data/mini_userbiz'):
        row = row.rstrip()

        userbiz_id, user_id, biz_id = row.split('\t')

        userbiz = UserBiz(user_id=int(user_id), biz_id=int(biz_id))

        # Add each user-biz relationship to the session
        db.session.add(userbiz)

    # Commit at end
    db.session.commit()


def load_biz():
    """Load businesses from mini_user into database."""

    print "Business"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Business.query.delete()

    # Read user file and insert data
    for row in open('data/mini_biz'):
        row = row.rstrip()

        biz_id, biz_name, address, city, state, country, zipcode, email, valid_email, phone, days_open, open_time, close_time, claimed = row.split('\t')

        biz = Business(biz_name=biz_name,
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
                       claimed = claimed)

        # Add each business to the session
        db.session.add(rbiz)

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
    load_movies()
    load_ratings()
    set_val_user_id()