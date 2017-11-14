"""Utility file to seed buddy database from fake data for demo."""

from sqlalchemy import func
from model import (User, Business, Friend, UserPromo, UserBiz, Review, Referral,
                   Promo, CheckIn, LikeReview, Invite, connect_to_db, db)

from datetime import datetime

from server import app

from faker import Faker

fake = Faker()


def create_users():
    """Create users data from Faker."""

    print 'Users'

    with open('data/users.txt', 'w+') as users:

        for i in range(250):
            users.write('{}|{}|{}|{}|{}|{}|{}|{}\n'.format(fake.user_name(),
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
                                                           fake.date(),
                                                           fake.date_this_decade(
                                                               before_today=True,
                                                               after_today=False),
                                                           fake.boolean(
                                                               chance_of_getting_true=10)))


def create_biz():
    """Create businesses data from Faker."""

    print 'Businesses'

    with open('data/biz.txt', 'w+') as biz:

        for i in range(100):
            biz.write('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n'.
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

    print 'Friends'

    with open('data/friends.txt', 'w+') as friends:

        for i in range(150):
            user_id = fake.random_int(min=1, max=250)

            friend_id = fake.random_int(min=1, max=250)

            while user_id == friend_id:
                friend_id = fake.random_int(min=1, max=250)

            friends.write('{}|{}\n'.format(user_id, friend_id))


def create_userbiz():
    """Create user-business relationships from Faker."""

    print 'User-Biz'

    with open('data/userbiz.txt', 'w+') as userbiz:

        for i in range(50):
            userbiz.write('{}|{}\n'.format(fake.random_int(min=1, max=250),
                                           fake.random_int(min=1, max=100)))


def create_promos():
    """Create promos from Faker."""

    print 'Promos'

    with open('data/promos.txt', 'w+') as promos:

        for i in range(100):
            promos.write('{}|{}|{}|{}\n'.format(fake.random_int(min=1, max=100),
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


def create_checkins():
    """Create check-ins from Faker."""

    print 'Check-Ins'

    with open('data/checkins.txt', 'w+') as checkins:

        for i in range(500):
            checkins.write('{}|{}|{}\n'.format(fake.random_int(min=1, max=250),
                                               fake.random_int(min=1, max=100),
                                               fake.date_this_decade(before_today=True,
                                                                   after_today=False)))


def create_referrals():
    """Create referrals relationships from Faker."""

    print 'Referrals'

    with open('data/referrals.txt', 'w+') as referrals:

        for i in range(100):
            referer_id = fake.random_int(min=1, max=250)

            referee_id = fake.random_int(min=1, max=250)

            while referer_id == referee_id:
                referee_id = fake.random_int(min=1, max=250)

            referrals.write('{}|{}|{}|{}\n'.format(referer_id, referee_id,
                                                   fake.random_int(min=1, max=100),
                                                   fake.date_this_decade(before_today=True,
                                                                         after_today=False),
                                                   i + 1))

            with open('data/userpromos.txt', 'w+') as userpromos:

                redeemed = fake.boolean(chance_of_getting_true=20)

                if redeemed:
                    redeem_date = fake.date_this_decade(before_today=True, after_today=False)
                else:
                    redeem_date = None

                userpromos.write('{}|{}|{}|{}\n'.format(referee_id,
                                                        fake.random_int(min=1, max=100),
                                                        redeemed,
                                                        redeem_date))
            # each instantiation results in userpromo_id and respective referee_id
            # into user_promo table; FIXME: to add in userpromo_id


def create_userpromos():
    """Create user-promotions relationships from Faker."""

    print 'User-Promos'

    with open('data/userpromos.txt', 'a+') as userpromos:

        for i in range(100):
            redeemed = fake.boolean(chance_of_getting_true=20)

            if redeemed:
                redeem_date = fake.date_this_decade(before_today=True, after_today=False)
            else:
                redeem_date = None

            userpromos.write('{}|{}|{}|{}\n'.format(fake.random_int(min=1, max=250),
                                                    fake.random_int(min=1, max=100),
                                                    redeemed,
                                                    redeem_date))


def create_reviews():
    """Create reviews from Faker."""

    print 'Reviews'

    with open('data/reviews.txt', 'w+') as reviews:

        for i in range(150):
            dispute = fake.boolean(chance_of_getting_true=20)

            if dispute:
                response = fake.text(max_nb_chars=5000, ext_word_list=None)
                revise_review = fake.boolean(chance_of_getting_true=30)
                if revise_review:
                    new_rating = fake.random_int(min=1, max=5)
                    new_review = fake.text(max_nb_chars=3000, ext_word_list=None)
                else:
                    cust_svc = fake.random_int(min=1, max=5)
            else:
                response = None
                revise_review = None
                new_rating = None
                new_review = None
                cust_svc = None

            reviews.write('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n'.format(fake.random_int(min=1, max=250),
                                                                   fake.random_int(min=1, max=100),
                                                                   fake.random_int(min=1, max=5),
                                                                   fake.text(max_nb_chars=5000,
                                                                             ext_word_list=None),
                                                                   fake.date_this_decade(before_today=True,
                                                                             after_today=False),
                                                                   dispute,
                                                                   response,
                                                                   revise_review,
                                                                   new_rating,
                                                                   new_review,
                                                                   cust_svc))


def create_likes():
    """Create likes of reviews from Faker."""

    print 'Likes'

    with open('data/likes.txt', 'w+') as likes:

        for i in range(150):
            likes.write('{}|{}\n'.format(fake.random_int(min=1, max=150),
                                         fake.random_int(min=1, max=250)))


def create_invites():
    """Create invites from Faker."""

    print 'Invites'

    with open('data/invites.txt', 'w+') as invites:

        for i in range(100):
            invites.write('{}|{}|{}\n'.format(fake.random_int(min=1, max=250),
                                              fake.free_email(),
                                              fake.boolean(chance_of_getting_true=30)))
            # if accepted is True, override email with respective email from friend_id
            # to also match with some of the friends table data


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
                       claimed=claimed,
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

    # Create fake data
    create_users()
    create_biz()
    create_friends()
    create_userbiz()
    create_promos()
    create_checkins()
    create_referrals()
    create_userpromos()
    create_reviews()
    create_likes()
    create_invites()

    # Import different types of data
    # load_users()
    # load_friends()
    # load_biz()
    # load_userbiz()
    # load_promos()
    # load_userpromos()
    # load_checkin()
    # load_referrals()
    # load_reviews()
    # load_likes()
    # load_invite()
    # set_val_user_id()