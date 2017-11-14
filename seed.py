"""Utility file to seed buddy database from fake data for demo."""

from sqlalchemy import func
from model import (User, Business, Friend, UserPromo, UserBiz, Review, Referral,
                   Redemption, Promo, CheckIn, LikeReview, Invite, connect_to_db, db)

from datetime import datetime

from server import app

from faker import Faker

fake = Faker()

def create_users():
    """Create users data from Faker."""

    with open('users.txt', 'r+') as users:

        for i in range(250):
            users.write('{}|{}|{}|{}|{}|{}|{}|{}'.format(fake.user_name(),
                                                         fake.first_name(),
                                                         fake.last_name(),
                                                         fake.free_email(),
                                                         fake.boolean(
                                                             chance_of_getting_true=99),
                                                         fake.password(length=10,
                                                             special_chars=True,
                                                             digits=True,
                                                             upper_case=True,
                                                             lower_case=True),
                                                         fake.image_url(width=None, height=None),
                                                         fake.birthdate(),
                                                         fake.date_this_decade(
                                                             before_today=True,
                                                             after_today=False),
                                                         fake.boolean(
                                                             chance_of_getting_true=10)))


def create_biz():
    """Create businesses data from Faker."""

    with open('biz.txt', 'r+') as biz:

        for i in range(100):
            biz.write('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.
                format(fake.company(),
                       fake.street_address(),
                       fake.city(),
                       fake.state_abbr(),
                       fake.country_code(),
                       fake.zipcode(),
                       fake.phone_number(),
                       fake.company_email(),
                       fake.boolean(chance_of_getting_true=99),
                       fake.url(),
                       fake.random_element(elements=('bar', 'cleaner', 'cafe',
                                                     'grocery', 'florist', 'home',
                                                     'medicine', 'nightlife',
                                                     'pet', 'restaurant', 'salon',
                                                     'spa')),
                       fake.random_element(elements=('M-F', 'M-S', 'M-Su', 'T-Su',
                                                     'M, W, F', 'S-Su', 'T-S')),
                       fake.random_int(min=1, max=24),
                       fake.random_int(min=0, max=24),
                       fake.boolean(chance_of_getting_true=50),
                       fake.image_url(width=None, height=None),
                       fake.longitude(),
                       fake.latitude()))


def create_friends():
    """Create friends relationships from Faker."""

    with open('friends.txt', 'r+') as friends:

        for i in range(150):
            friends.write('{}|{}'.format(fake.random_int(min=1, max=250),
                                         fake.random_int(min=1, max=250)))


def create_userbiz():
    """Create user-business relationships from Faker."""

    with open('userbiz.txt', 'r+') as userbiz:

        for i in range(50):
            userbiz.write('{}|{}'.format(fake.random_int(min=1, max=250),
                                         fake.random_int(min=1, max=100)))


def create_promos():
    """Create promos from Faker."""

    with open('promos.txt', 'r+') as promos:

        for i in range(100):
            promos.write('{}|{}|{}|{}'.format(fake.random_int(min=1, max=100),
                                              fake.word(ext_word_list=None),
                                              fake.sentence(nb_words=5,
                                                            variable_nb_words=True,
                                                            ext_word_list=None),
                                              fake.date_this_decade(before_today=True,
                                                                    after_today=False),
                                              fake.time_delta(end_datetime=None),
                                              fake.boolean(chance_of_getting_true=10),
                                              fake.boolean(chance_of_getting_true=10),
                                              fake.random_digit_or_empty()))


def load_users():
    """Load users from fake data into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read user file and insert data
    for row in open('data/users'):
        row = row.rstrip()

        user_id, username, first_name, last_name, email, valid_email, password, dob_str, join_date_str, biz_acct = row.split('|')

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
    """Load friends relationship from fake data into database."""

    print "Friends"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Friend.query.delete()

    # Read user file and insert data
    for row in open('data/friends'):
        row = row.rstrip()

        link_id, user_id, friend_id = row.split('|')

        friend = Friend(user_id=int(user_id), friend_id=int(friend_id))

        # Add each friend relationship to the session
        db.session.add(friend)

    # Commit at end
    db.session.commit()


def load_userbiz():
    """Load user-biz relationship from fake data into database."""

    print "UserBiz"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    UserBiz.query.delete()

    # Read user file and insert data
    for row in open('data/userbiz'):
        row = row.rstrip()

        userbiz_id, user_id, biz_id = row.split('|')

        userbiz = UserBiz(user_id=int(user_id), biz_id=int(biz_id))

        # Add each user-biz relationship to the session
        db.session.add(userbiz)

    # Commit at end
    db.session.commit()


def load_biz():
    """Load businesses from fake data into database."""

    print "Business"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Business.query.delete()

    # Read user file and insert data
    for row in open('data/biz'):
        row = row.rstrip()

        biz_id, biz_name, address, city, state, country, zipcode, email, valid_email, phone, days_open, open_time, close_time, claimed = row.split('|')

        biz = Business(biz_name=biz_name,
                       address=address,
                       city=city,
                       state=state,
                       country=country,
                       zipcode=zipcode,
                       email=email,
                       valid_email=valid_email,
                       url=url,
                       phone=phone,
                       days_open=days_open,
                       open_time=int(open_time),
                       close_time=int(close_time),
                       claimed = claimed,
                       biz_pic=pic)

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