"""Utility file to seed buddy database from fake data for demo."""

from sqlalchemy import func
from model import (User, Business, Friend, UserPromo, UserBiz, Review, Referral,
                   Promo, CheckIn, LikeReview, Invite, connect_to_db, db)
from datetime import datetime
from server import app
from faker import Faker
from data.markov.markov import make_title_descr, make_text, MARKOV_CHAIN
import re

fake = Faker()


def create_users():
    """Creates users data from Faker.

    Note: Overrode with data from mockaroo API for consistency of user.
    """

    print 'Users'

    with open('data/users.txt', 'w+') as users:

        for i in range(500):
            users.write('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n'.format(fake.user_name(),
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
    """Creates businesses data from Faker.

    Note: Overrode with data from mockaroo API for consistency of business.
    """

    print 'Businesses'

    with open('data/biz.txt', 'w+') as biz:

        for i in range(1000):
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
                       fake.random_element(elements=('Bar', 'Cleaners', 'Coffee/Cafe/Tea',
                                                     'Deli/Grocery', 'Florist', 'Home Services',
                                                     'Medical Services', 'Legal Services',
                                                     'Nightlife', 'Pets', 'Restaurant',
                                                     'Salon', 'Spa')),
                       fake.random_element(elements=('M-F', 'M-S', 'M-Su', 'T-Su',
                                                     'M, W, F', 'S-Su', 'T-S')),
                       fake.random_int(min=1, max=24),
                       fake.random_int(min=0, max=24),
                       fake.boolean(chance_of_getting_true=50),
                       fake.image_url(width=None, height=None),
                       fake.longitude(),
                       fake.latitude()))


def create_friends():
    """Creates friends relationships from Faker."""

    print 'Friends'

    with open('data/friends.txt', 'w+') as friends:

        for i in range(1000):
            user_id = fake.random_int(min=1, max=500)

            friend_id = fake.random_int(min=1, max=500)

            while user_id == friend_id:
                friend_id = fake.random_int(min=1, max=500)

            friends.write('{}|{}\n'.format(user_id, friend_id))


def create_userbiz():
    """Creates user-business relationships from Faker."""

    print 'User-Biz'

    with open('data/userbiz.txt', 'w+') as userbiz:

        for i in range(500):
            userbiz.write('{}|{}\n'.format(fake.random_int(min=1, max=500),
                                           fake.random_int(min=1, max=1000)))


def create_promos():
    """Creates promos from Faker.

    Note: Overrode with data from mockaroo.
    """

    print 'Promos'

    with open('data/promos.txt', 'w+') as promos:

        for i in range(5000):

            title = make_title_descr(MARKOV_CHAIN, 4)
            descr = make_title_descr(MARKOV_CHAIN, 8)
            start_date = fake.date_this_decade(before_today=True, after_today=False)
            end_date = fake.date_between_dates(date_start=start_date, date_end=None)

            promos.write('{}|{}|{}|{}|{}|{}|{}|{}\n'.format(fake.random_int(min=1, max=1000),
                                                            title,
                                                            descr,
                                                            start_date,
                                                            end_date,
                                                            fake.boolean(chance_of_getting_true=10),
                                                            fake.boolean(chance_of_getting_true=10),
                                                            fake.random_int(min=0, max=1500)))


def create_checkins():
    """Creates check-ins from Faker."""

    print 'Check-Ins'

    with open('data/checkins.txt', 'w+') as checkins:

        for i in range(300000):
            checkins.write('{}|{}|{}\n'.format(fake.random_int(min=1, max=500),
                                               fake.random_int(min=1, max=1000),
                                               fake.date_this_decade(before_today=True,
                                                                     after_today=False)))


def create_referrals():
    """Creates referrals relationships from Faker."""

    print 'Referrals'

    with open('data/referrals.txt', 'w+') as referrals:
        with open('data/userpromos.txt', 'w+') as userpromos:

            for i in range(75000):
                referer_id = fake.random_int(min=1, max=500)

                referee_id = fake.random_int(min=1, max=500)

                while referer_id == referee_id:
                    referee_id = fake.random_int(min=1, max=500)

                referrals.write('{}|{}|{}|{}|{}\n'.format(referer_id, referee_id,
                                                          fake.random_int(min=1, max=1000),
                                                          fake.date_this_decade(before_today=True,
                                                                                after_today=False),
                                                          i + 1),
                                                          fake.boolean(chance_of_getting_true=70))

                redeemed = fake.boolean(chance_of_getting_true=50)

                if redeemed:
                    redeem_date = fake.date_this_decade(before_today=True, after_today=False)
                else:
                    redeem_date = ''

                userpromos.write('{}|{}|{}|{}\n'.format(referee_id,
                                                        fake.random_int(min=1, max=5000),
                                                        redeemed,
                                                        redeem_date))


def create_userpromos():
    """Creates user-promotions relationships from Faker."""

    print 'User-Promos'

    with open('data/userpromos.txt', 'a') as userpromos:

        for i in range(10000):
            redeemed = fake.boolean(chance_of_getting_true=40)

            if redeemed:
                redeem_date = fake.date_this_decade(before_today=True, after_today=False)
            else:
                redeem_date = ''

            userpromos.write('{}|{}|{}|{}\n'.format(fake.random_int(min=1, max=500),
                                                    fake.random_int(min=1, max=1000),
                                                    redeemed,
                                                    redeem_date))


def create_reviews():
    """Creates reviews from Faker."""

    print 'Reviews'

    with open('data/reviews.txt', 'w+') as reviews:

        for i in range(7500):

            review = make_text(MARKOV_CHAIN, 1000, 5000)

            dispute = fake.boolean(chance_of_getting_true=20)

            if dispute:
                response = make_text(MARKOV_CHAIN, 1000, 5000)  # fake.text(max_nb_chars=5000, ext_word_list=None)
                revise_review = fake.boolean(chance_of_getting_true=30)
                if revise_review:
                    new_rating = fake.random_int(min=1, max=5)
                    new_review = make_text(MARKOV_CHAIN, 1000, 3000)  # fake.text(max_nb_chars=3000, ext_word_list=None)
                    cust_svc = ''
                else:
                    cust_svc = fake.random_int(min=1, max=5)
                    new_rating = ''
                    new_review = ''
            else:
                response = ''
                revise_review = ''
                new_rating = ''
                new_review = ''
                cust_svc = ''

            reviews.write('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n'.format(fake.random_int(min=1, max=500),
                                                                      fake.random_int(min=1, max=1000),
                                                                      fake.random_int(min=1, max=5),
                                                                      review,
                                                                      fake.date_this_decade(before_today=True,
                                                                                            after_today=False),
                                                                      dispute,
                                                                      response,
                                                                      revise_review,
                                                                      new_rating,
                                                                      new_review,
                                                                      cust_svc))


def create_likes():
    """Creates likes of reviews from Faker."""

    print 'Likes'

    with open('data/likes.txt', 'w+') as likes:

        for i in range(50000):
            likes.write('{}|{}\n'.format(fake.random_int(min=1, max=7500),
                                         fake.random_int(min=1, max=500)))


def create_invites():
    """Creates invites from Faker."""

    print 'Invites'

    with open('data/invites.txt', 'w+') as invites:

        for i in range(1000):
            invites.write('{}|{}|{}\n'.format(fake.random_int(min=1, max=500),
                                              fake.free_email(),
                                              fake.boolean(chance_of_getting_true=30)))


def load_users():
    """Loads users from fake data into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read user file and insert data
    for row in open('data/users.txt', 'rU'):
        row = row.rstrip()

        (username, first_name, last_name, email, valid_email, password, pic,
         dob_str, join_date_str, biz_acct) = row.split('|')

        # Convert to datetime format
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        join_date = datetime.strptime(join_date_str, '%Y-%m-%d')

        # Convert from string to boolean
        if valid_email == 'true':
            valid_email = True
        else:
            valid_email = False

        if biz_acct == 'true':
            biz_acct = True
        else:
            biz_acct = False

        user = User(username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    valid_email=valid_email,
                    password=password,
                    user_pic=pic,
                    dob=dob,
                    join_date=join_date,
                    biz_acct=biz_acct)

        # Add each user to the session
        db.session.add(user)

    # Commit at end
    db.session.commit()


def load_friends():
    """Loads friends relationship from fake data into database."""

    print "Friends"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Friend.query.delete()

    # Read user file and insert data
    for row in open('data/friends.txt', 'rU'):
        row = row.rstrip()

        user_id, friend_id = row.split('|')

        friend = Friend(user_id=int(user_id), friend_id=int(friend_id))

        # Add each friend relationship to the session
        db.session.add(friend)

    # Commit at end
    db.session.commit()


def load_userbiz():
    """Loads user-biz relationship from fake data into database."""

    print "UserBiz"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    UserBiz.query.delete()

    # Read user file and insert data
    for row in open('data/userbiz.txt', 'rU'):
        row = row.rstrip()

        user_id, biz_id = row.split('|')

        userbiz = UserBiz(user_id=int(user_id), biz_id=int(biz_id))

        # Add each user-biz relationship to the session
        db.session.add(userbiz)

    # Commit at end
    db.session.commit()


def load_biz():
    """Load businesses from fake data into database."""

    print 'Businesses'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Business.query.delete()

    # Read user file and insert data
    for row in open('data/biz.txt', 'rU'):
        row = row.rstrip()

        (biz_name, address, city, state, country, zipcode, phone, email,
         valid_email, url, category, days_open, open_time, close_time, claimed,
         biz_pic, longitude, latitude) = row.split('|')

        # Convert phone to same format
        re.sub('\ |\?|\.|\!|\/|\;|\:|\-|\(|\)', '', phone)

        # Convert from string to boolean
        if valid_email == 'true':
            valid_email = True
        else:
            valid_email = False

        if claimed == 'true':
            claimed = True
        else:
            claimed = False

        open_time = open_time[:-3]
        close_time = close_time[:-3]

        biz = Business(biz_name=biz_name,
                       address=address,
                       city=city,
                       state=state,
                       country=country,
                       zipcode=zipcode,
                       phone=phone,
                       email=email,
                       valid_email=valid_email,
                       url=url,
                       category=category,
                       days_open=days_open,
                       open_time=int(open_time),
                       close_time=int(close_time),
                       claimed=claimed,
                       biz_pic=biz_pic,
                       lng=float(longitude),
                       lat=float(latitude),
                       location='POINT({} {})'.format(longitude, latitude))

        # Add each business to the session
        db.session.add(biz)

    # Commit at end
    db.session.commit()


def load_promos():
    """Loads promos from fake promos into database."""

    print 'Promos'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Promo.query.delete()

    # Read user file and insert data
    for row in open('data/promos.txt', 'rU'):
        row = row.rstrip()

        biz_id, title, descr, start_date_str, end_date_str, referral, birthday, redeem_count = row.split('|')

        # Convert to datetime format
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        # start_date = datetime.strptime(start_date_str, '%m/%d/%y')
        # end_date_str = end_date_str[:10]
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        # Convert from string to boolean
        if referral == 'true':
            referral = True
        else:
            referral = False

        if birthday == 'true':
            birthday = True
        else:
            birthday = False

        # Convert redeem_count to

        promo = Promo(biz_id=int(biz_id),
                      title=title,
                      descr=descr,
                      start_date=start_date,
                      end_date=end_date,
                      referral_promo=referral,
                      birthday_promo=birthday,
                      redeem_count=int(redeem_count))

        # Add each promo to the session
        db.session.add(promo)

    # Commit at end
    db.session.commit()


def load_userpromos():
    """Loads user-promos relationship from fake data in database."""

    print 'User-Promos'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    UserPromo.query.delete()

    # Read user file and insert data
    for row in open('data/userpromos.txt', 'rU'):
        row = row.rstrip()

        user_id, promo_id, redeemed, redeem_date_str = row.split('|')

        # Convert to datetime format
        if redeem_date_str:
            redeem_date = datetime.strptime(redeem_date_str, '%Y-%m-%d')
        else:
            redeem_date = None

        # Convert from string to boolean
        if redeemed == 'True':
            redeemed = True
        else:
            redeemed = False

        userpromo = UserPromo(user_id=user_id,
                              promo_id=promo_id,
                              redeemed=redeemed,
                              redeem_date=redeem_date)

        # Add each user-promo to the session
        db.session.add(userpromo)

    # Commit at end
    db.session.commit()


def load_checkins():
    """Loads check-ins from fake data in database."""

    print 'Check-Ins'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    CheckIn.query.delete()

    # Read user file and insert data
    for row in open('data/checkins.txt', 'rU'):
        row = row.rstrip()

        user_id, biz_id, checkin_date_str = row.split('|')

        # Convert to datetime format
        checkin_date = datetime.strptime(checkin_date_str, '%Y-%m-%d')

        checkin = CheckIn(user_id=int(user_id),
                          biz_id=int(biz_id),
                          checkin_date=checkin_date)

        # Add each check-in to the session
        db.session.add(checkin)

    # Commit at end
    db.session.commit()


def load_referrals():
    """Loads referrals from fake data in database."""

    print 'Referrals'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Referral.query.delete()

    # Read user file and insert data
    for row in open('data/referrals.txt', 'rU'):
        row = row.rstrip()

        referer_id, referee_id, biz_id, refer_date_str, userpromo_id, redeemed = row.split('|')

        # Convert to datetime format
        refer_date = datetime.strptime(refer_date_str, '%Y-%m-%d')

        # Convert from string to boolean
        if redeemed == 'True':
            redeemed = True
        else:
            redeemed = False

        referral = Referral(referer_id=int(referer_id),
                            referee_id=int(referee_id),
                            biz_id=int(biz_id),
                            refer_date=refer_date,
                            userpromo_id=int(userpromo_id),
                            redeemed=redeemed)

        # Add each referral to the session
        db.session.add(referral)

    # Commit at end
    db.session.commit()


def load_reviews():
    """Loads reviews from fake data in database."""

    print 'Reviews'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Review.query.delete()

    # Read user file and insert data
    for row in open('data/reviews.txt', 'rU'):
        row = row.rstrip()

        (user_id, biz_id, rating, review, review_date_str, dispute, response,
            revise_review, new_rating, new_review, cust_svc) = row.split('|')

        # Convert to datetime format
        review_date = datetime.strptime(review_date_str, '%Y-%m-%d')

        # Convert from string to boolean
        if dispute == 'True':
            dispute = True
        else:
            dispute = False

        if revise_review == 'True':
            revise_review = True
        else:
            revise_review = False

        # Convert from string to integer
        if new_rating:
            new_rating = int(new_rating)
        else:
            new_rating = None

        if cust_svc:
            cust_svc = int(cust_svc)
        else:
            cust_svc = None

        review = Review(user_id=int(user_id),
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
    """Loads likes of reviews from fake data into database."""

    print 'Likes'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    LikeReview.query.delete()

    # Read user file and insert data
    for row in open('data/likes.txt', 'rU'):
        row = row.rstrip()

        review_id, user_id = row.split('|')

        like = LikeReview(user_id=int(user_id), review_id=int(review_id))

        # Add each like transaction to the session
        db.session.add(like)

    # Commit at end
    db.session.commit()


def load_invites():
    """Loads friends relationship from fake data into database."""

    print 'Invites'

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Invite.query.delete()

    # Read user file and insert data
    for row in open('data/invites.txt', 'rU'):
        row = row.rstrip()

        user_id, friend_email, accepted = row.split('|')

        if accepted == 'True':
            accepted = True
        else:
            accepted = False

        invite = Invite(user_id=int(user_id), friend_email=friend_email, accepted=accepted)

        # Add each invite to the session
        db.session.add(invite)

    # Commit at end
    db.session.commit()


def set_val_id():
    """Sets value for the next autoincrement after seeding database"""

    # Get the Max autoincremented primary key in the database
    result = db.session.query(func.max(User.user_id)).one()
    user_max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': user_max_id + 1})

    # Get the Max autoincremented primary key in the database
    result = db.session.query(func.max(Business.biz_id)).one()
    biz_max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('businesses_biz_id_seq', :new_id)"
    db.session.execute(query, {'new_id': biz_max_id + 1})

    # Get the Max autoincremented primary key in the database
    result = db.session.query(func.max(Friend.link_id)).one()
    friend_max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('friends_link_id_seq', :new_id)"
    db.session.execute(query, {'new_id': friend_max_id + 1})

    # Get the Max autoincremented primary key in the database
    result = db.session.query(func.max(UserBiz.userbiz_id)).one()
    userbiz_max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('user_biz_userbiz_id_seq', :new_id)"
    db.session.execute(query, {'new_id': userbiz_max_id + 1})

    # Get the Max autoincremented primary key in the database
    result = db.session.query(func.max(Promo.promo_id)).one()
    promo_max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('promos_promo_id_seq', :new_id)"
    db.session.execute(query, {'new_id': promo_max_id + 1})

    # Get the Max autoincremented primary key in the database
    result = db.session.query(func.max(UserPromo.userpromo_id)).one()
    userpromo_max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('user_promos_userpromo_id_seq', :new_id)"
    db.session.execute(query, {'new_id': userpromo_max_id + 1})

    # Get the Max autoincremented primary key in the database
    result = db.session.query(func.max(CheckIn.checkin_id)).one()
    checkins_max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('checkins_checkin_id_seq', :new_id)"
    db.session.execute(query, {'new_id': checkins_max_id + 1})

    # Get the Max autoincremented primary key in the database
    result = db.session.query(func.max(Referral.referral_id)).one()
    referral_max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('referrals_referral_id_seq', :new_id)"
    db.session.execute(query, {'new_id': referral_max_id + 1})

    # Get the Max autoincremented primary key in the database
    result = db.session.query(func.max(Review.review_id)).one()
    review_max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('reviews_review_id_seq', :new_id)"
    db.session.execute(query, {'new_id': review_max_id + 1})

    # Get the Max autoincremented primary key in the database
    result = db.session.query(func.max(LikeReview.like_id)).one()
    like_max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('likes_like_id_seq', :new_id)"
    db.session.execute(query, {'new_id': like_max_id + 1})

    # Get the Max autoincremented primary key in the database
    result = db.session.query(func.max(Invite.invite_id)).one()
    invites_max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('invites_invite_id_seq', :new_id)"
    db.session.execute(query, {'new_id': invites_max_id + 1})

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    # db.create_all()

    # Create fake data
    # create_users()
    # create_biz()
    # create_friends()
    # create_userbiz()
    # create_promos()
    # create_checkins()
    # create_referrals()
    # create_userpromos()
    # create_reviews()
    # create_likes()
    # create_invites()

    # Import different types of data
    load_users()
    load_friends()
    load_biz()
    load_userbiz()
    load_promos()
    load_userpromos()
    load_checkins()
    load_referrals()
    load_reviews()
    load_likes()
    load_invites()
    set_val_id()
