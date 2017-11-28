from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.ext.associationproxy import association_proxy  # FIXME: may not need
from sqlalchemy import func, distinct
from geoalchemy2 import Geometry
from datetime import datetime

db = SQLAlchemy()


##############################################################################
# Model definitions


class User(db.Model):
    """ User model. """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    valid_email = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(64), nullable=False)  # should encrypt
    user_pic = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.DateTime, nullable=True)
    join_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    # FIXME: not sure if current_timestamp syntax is correct for SQLAlchemy
    biz_acct = db.Column(db.Boolean, nullable=True)
    # FIXME: may not need, when user logs in, can do query of userbiz table for userid and store it all in businesses
    __table_args__ = (db.CheckConstraint("email ~ '^[A-Z0-9a-z._%+-]+@[A-Z0-9a-z.-]+\.[A-Za-z]{2,}$'"),)

    biz = db.relationship('Business', secondary='user_biz', backref='users')
    invites = db.relationship('Invite', backref='users')
    friends = db.relationship('User', secondary='friends',
                              primaryjoin='User.user_id == Friend.user_id',
                              secondaryjoin='User.user_id == Friend.friend_id')
    promos = db.relationship('Promo', secondary='user_promos', backref='users')
    checkins = db.relationship('CheckIn', backref='users')
    referees = db.relationship('User', secondary='referrals',
                               primaryjoin='User.user_id == Referral.referer_id',
                               secondaryjoin='User.user_id == Referral.referee_id',
                               backref='referer')
    referrals = db.relationship('Referral',
                                primaryjoin='Referral.referer_id == User.user_id',
                                backref='referer')
    referred = db.relationship('Referral',
                               primaryjoin='Referral.referee_id == User.user_id',
                               backref='referee')
    reviews = db.relationship('Review', backref='users')

    def __repr__(self):
        """Displays info"""

        return (u'<user_id={} username={} email={}>'.format(self.user_id,
                self.username, self.email))

    def tot_friends(self):
        """ Calculates total friends. """

        total = len(self.friends)

        return total

    def tot_reviews(self):
        """ Calculates total reviews of businesses. """

        total = len(self.reviews)

        return total

    def tot_checkins(self):
        """ Calculates total checkins to businesses. """

        total = len(self.checkins)

        return total

    def tot_refs(self):
        """ Calculates total referrals. """

        total = len(self.referrals)

        return total

    def tot_refs_reds(self):
        """ Calculates total referrals that have been redeemed. """

        redeemed = 0

        for referral in self.referrals:
            if referral.user_promo.redeemed is True:
                redeemed += 1

        return redeemed

    def tot_reds(self):
        """ Calculates total promotions that have been redeemed. """

        redeemed_promos = 0

        for promo in self.user_promos:
            if promo.redeemed is True:
                redeemed_promos += 1

        return redeemed_promos

    def tot_unique_biz(self):
        """ Calculates total of different business that have been checked into. """

        unique_biz = (db.session.query(func.count(distinct(CheckIn.biz_id)))
                      .filter_by(user_id=self.user_id).scalar())

        return unique_biz

    def tot_biz_referrals(self):
        """ Calculates total businesses that have been referred by user and redeemed by referee. """

        unique_biz_refs = (db.session.query(func.count(distinct(Referral.biz_id)))
                           .join(UserPromo).filter(UserPromo.redeemed == True,
                           UserPromo.user_id == self.user_id).scalar())

        return unique_biz_refs

    def deg_of_sep(self, user2_id, degrees=100):
        """
        Calculates degrees of separation, if any, between two users. If count is none, the user2 is user1. Otherwise, count of zero
        means no connection. Currently set to stop at count at n degrees.
        """

        tree = []
        sought = user2_id
        pop = self.user_id
        anchor = self.user_id
        count = 0

        while True:

            if pop == sought:
                if count == 0:
                    count = None
                return count
            else:
                update_tree(friends_lst(pop), tree)
                if pop == anchor:
                    if tree = []:
                        count = 0
                        return count
                    else:
                        anchor = tree[-1]
                        count += 1
                        if count == (degrees + 1):
                            return count
                pop = tree.pop(0)

        return count


class Friend(db.Model):
    """ Relationship information between user profiles. """

    __tablename__ = 'friends'

    link_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        """ Displays info. """

        return (u'<user_id={} friend_id={}>'.format(self.user_id, self.friend_id))


class UserBiz(db.Model):
    """ Relationship information between business user profile and related
    businesses that are claimed. """

    __tablename__ = 'user_biz'

    userbiz_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    biz_id = db.Column(db.Integer, db.ForeignKey('businesses.biz_id'))

    def __repr__(self):
        """ Displays info. """

        return (u'<user_id={} biz_id={}>'.format(self.user_id, self.biz_id))


class Business(db.Model):
    """ Business model. """

    __tablename__ = 'businesses'

    biz_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    biz_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(64), nullable=True)
    state = db.Column(db.String(64), nullable=True)
    country = db.Column(db.String(64), nullable=True)
    zipcode = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    valid_email = db.Column(db.Boolean, nullable=False, default=False)
    url = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(64), nullable=True)
    days_open = db.Column(db.String(64), nullable=True)
    open_time = db.Column(db.Integer, nullable=True)
    close_time = db.Column(db.Integer, nullable=True)
    claimed = db.Column(db.Boolean, nullable=False, default=False)
    biz_pic = db.Column(db.String(100), nullable=True)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    location = db.Column(Geometry(geometry_type='POINT'), nullable=True)
    __table_args__ = (db.CheckConstraint("email ~ '^[A-Z0-9a-z._%+-]+@[A-Z0-9a-z.-]+\.[A-Za-z]{2,}$'"),)

    checkins = db.relationship('CheckIn', backref='biz')
    referrals = db.relationship('Referral', backref='biz')
    reviews = db.relationship('Review', backref='biz')
    promos = db.relationship('Promo', backref='biz')

    def __repr__(self):
        """ Displays info. """

        return (u'<biz_id={} biz_name={}>'.format(self.biz_id, self.biz_name))

    def is_owned(self, user_id):
        """ Tracks whether business has been claimed by a specific user. """

        owned = UserBiz.query.filter(UserBiz.biz_id == self.biz_id, UserBiz.user_id == user_id).first()

        if owned:
            return True
        else:
            return False

    def is_claimed(self):
        """
        Tracks whether business has been claimed and therefore, is available
        to be claimed or not.
        """

        claimed = UserBiz.query.filter_by(biz_id=self.biz_id).first()

        if claimed:
            return True
        else:
            return False

    def is_checkin(self, user_id):
        """ Tracks whether business has been checked into by specific user for
        that day. """

        today = datetime.today().date()

        checkin = CheckIn.query.filter(CheckIn.biz_id == self.biz_id,
                                       CheckIn.user_id == user_id,
                                       CheckIn.checkin_date == today).first()

        if checkin:
            return True
        else:
            return False

    def has_reviewed(self, user_id):
        """ Tracks whether business has been reviewed by a specific user. """

        review = Review.query.filter(Review.biz_id == self.biz_id,
                                     Review.user_id == user_id).first()

        if review:
            return True
        else:
            return False

    def visit_not_reviewed(self, user_id):
        """ Tracks whether business has been checked in but not reviewed by
        specific user. """

        checkins_not_reviewed = (db.session.query(distinct(CheckIn.biz_id))
                                 .filter(CheckIn.user_id == user_id,
                                 CheckIn.biz_id.notin_(db
                                 .session.query(distinct(Review.biz_id))
                                 .filter(Review.user_id == user_id))).all())

        not_reviewed = False

        for item in checkins_not_reviewed:
            if item[0] == self.biz_id:
                not_reviewed = True

        return not_reviewed

    def tot_checkins(self):
        """ Tracks total check-ins to the business. """

        total = len(self.checkins)

        return total

    def tot_user_checkins(self, user_id):
        """ Tracks total check-ins to the business by a specific user. """

        total = CheckIn.query.filter(CheckIn.user_id == user_id,
                CheckIn.biz_id == self.biz_id).count()

        return total

    def tot_reviews(self):
        """ Calculates total reviews for a business. """

        count = len(self.reviews)

        return count

    def avg_score(self):
        """ Calculates average rating of business. """

        tot_score = 0

        for review in self.reviews:
            if review.revise_review:
                tot_score += review.new_rating
            else:
                tot_score += review.rating

        avg_rating = tot_score / self.tot_reviews()

        return avg_rating

    def tot_promos_red(self):
        """ Calculates total promotions redeemed by consumers. """

        redeemed_promos = 0

        for promo in self.promos:
            for item in promo.user_promos:
                if item.redeemed is True:
                    redeemed_promos += 1

        return redeemed_promos

    def tot_refs(self):
        """ Calculates total referrals. """

        total = len(self.referrals)

        return total

    def tot_refs_red(self):
        """ Calculates total referrals that have been redeemed. """

        redeemed_refs = 0

        for item in self.referrals:
            if item.user_promo.redeemed is True:
                redeemed_refs += 1

        return redeemed_refs

    def deg_of_sep(self, user2_id, degrees=100):
        """
        Calculates degrees of separation, if any, between a user and business,
        if claimed. If count is none, the user2 is user1. Otherwise, count of zero
        means no connection. Currently set to stop at count at n degrees.
        """

        if not self.users:
            return None
        else:
            tree = []
            sought = user2_id
            pop = self.users[0].user_id
            anchor = self.users[0].user_id
            count = 0

            while True:

                if pop == sought:
                    if count == 0:
                        count = None
                    return count
                else:
                    update_tree(friends_lst(pop), tree)
                    if pop == anchor:
                        if tree = []:
                            count = 0
                            return count
                        else:
                            anchor = tree[-1]
                            count += 1
                            if count == (degrees + 1):
                                return count
                    pop = tree.pop(0)

                return count


class Promo(db.Model):
    """ Promotions model. """

    __tablename__ = 'promos'

    promo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    biz_id = db.Column(db.Integer, db.ForeignKey('businesses.biz_id'))
    title = db.Column(db.String(64), nullable=False)
    descr = db.Column(db.String(100), nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    referral_promo = db.Column(db.Boolean, nullable=False, default=False)
    birthday_promo = db.Column(db.Boolean, nullable=False, default=False)
    redeem_count = db.Column(db.Integer, nullable=False, default=None)

    def __repr__(self):
        """ Displays info. """

        return (u'<promo_id={} biz_id={} title={} end_date={}>'
                .format(self.promo_id, self.biz_id, self.title, self.end_date))


class UserPromo(db.Model):
    """ Relationship information between user and related promotions. """

    __tablename__ = 'user_promos'

    userpromo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    promo_id = db.Column(db.Integer, db.ForeignKey('promos.promo_id'))
    redeemed = db.Column(db.Boolean, nullable=False, default=False)
    redeem_date = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', backref='user_promos')
    promo = db.relationship('Promo', backref='user_promos')
    # User.promos = association_proxy('user_promos', 'promos')
    # Promo.users = association_proxy('user_promos', 'users')

    def __repr__(self):
        """ Displays info. """

        return (u'<userpromo_id={} user_id={} promo_id={} redeemed={}>'
                .format(self.userpromo_id, self.user_id, self.promo_id, self.redeemed))


class CheckIn(db.Model):
    """ Check-in model. """

    __tablename__ = 'checkins'

    checkin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    biz_id = db.Column(db.Integer, db.ForeignKey('businesses.biz_id'))
    checkin_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        """ Displays info. """

        return (u'<checkin_id={} user_id={} biz_id={} checkin_date={}>'
                .format(self.checkin_id, self.user_id, self.biz_id, self.checkin_date))


class Referral(db.Model):
    """ Referral model. """

    __tablename__ = 'referrals'

    referral_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    referer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    referee_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    biz_id = db.Column(db.Integer, db.ForeignKey('businesses.biz_id'))
    refer_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    userpromo_id = db.Column(db.Integer, db.ForeignKey('user_promos.userpromo_id'))

    user_promo = db.relationship('UserPromo', backref='referral')

    def __repr__(self):
        """ Displays info. """

        return (u'<referral_id={} biz_id={} refer_date={} userpromo_id={}>'
                .format(self.referral_id, self.biz_id, self.refer_date, self.userpromo_id))

    def referee(self):
        """ Tracks referees that have been referred to the specific business. """

        user = User.query.filter_by(user_id=self.referee_id).first()

        return user.username


class Review(db.Model):
    """ Review model. """

    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    biz_id = db.Column(db.Integer, db.ForeignKey('businesses.biz_id'))
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(5000), nullable=False)
    review_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    # same re: timestamp
    dispute = db.Column(db.Boolean, nullable=False, default=False)
    response = db.Column(db.String(5000), nullable=True)
    revise_review = db.Column(db.Boolean, nullable=True)
    new_rating = db.Column(db.Integer, nullable=True)
    new_review = db.Column(db.String(3000), nullable=True)
    cust_svc = db.Column(db.Integer, nullable=True)
    __table_args__ = (db.CheckConstraint('rating >= 1'), db.CheckConstraint('rating <= 5'),
                      db.CheckConstraint('new_rating >= 1'), db.CheckConstraint('new_rating <= 5'),
                      db.CheckConstraint('cust_svc >= 1'), db.CheckConstraint('cust_svc <= 5'))

    def __repr__(self):
        """ Displays info. """

        return (u'<review_id={} user_id={} biz_id={} rating={}>'
                .format(self.review_id, self.user_id, self.biz_id, self.rating))

    def has_liked(self, user_id):
        """ Tracks whether review has been liked by a certain user. """

        user_like = LikeReview.query.filter(LikeReview.review_id == self.review_id,
                                            LikeReview.user_id == user_id).first()

        if user_like:
            return True
        else:
            return False

    def tot_likes(self):
        """ Calculates total likes per review. """

        total = (db.session.query(func.count(LikeReview.like_id))
                 .filter_by(review_id=self.review_id).scalar())

        return total


class LikeReview(db.Model):
    """ Tracks user 'likes' of individual reviews by business. """

    __tablename__ = 'likes'

    like_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.review_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        """ Displays info. """

        return (u'<review_id={} user_id={}>'.format(self.review_id, self.user_id))


class Invite(db.Model):
    """ User invite model. """

    __tablename__ = 'invites'

    invite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    friend_email = db.Column(db.String(64), nullable=False)
    accepted = db.Column(db.Boolean, nullable=False, default=False)
    __table_args__ = (db.CheckConstraint("friend_email ~ '^[A-Z0-9a-z._%+-]+@[A-Z0-9a-z.-]+\.[A-Za-z]{2,}$'"),)
    # data modeling lecture, look at many to many demo, instantiate book and user and comment link

    def __repr__(self):
        """ Displays info. """

        return (u'<invite_id={} user_id={} accepted={}'
                .format(self.invite_id, self.user_id, self.accepted))


def friends_lst(user_id):
    """
    Returns list of friends' user_id.

    TO DO: Build out doctests
    """

    lst = []

    friends = db.session.query(Friend.friend_id).filter_by(user_id=user_id).all()

    for friend in friends:
        lst.append(friend)

    return lst


def update_tree(friends_lst, tree):
    """
    Update connections for new list of friends for degrees of separation calculation.

    TO DO: Build out doctests
    """

    for friend in friends_lst:
        tree.append(friend)

    return tree


##############################################################################
# Helper functions

def connect_to_db(app, db_uri='postgresql:///buddy'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

    db.create_all()
