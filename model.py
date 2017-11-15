from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy  # FIXME: may not need
from sqlalchemy import func
from geoalchemy2 import Geometry

db = SQLAlchemy()

# use func from sqlalchemy (lower case)

##############################################################################
# Model definitions

class User(db.Model):
    """ User model. """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = (db.Column(db.String(64), nullable=False, unique=True))
    valid_email = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(64), nullable=False)  # should encrypt
    user_pic = db.Column(db.String(64), nullable=True)
    dob = db.Column(db.DateTime, nullable=True)
    join_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    # FIXME: not sure if current_timestamp syntax is correct for SQLAlchemy
    biz_acct = db.Column(db.Boolean, nullable=True)
    # FIXME: may not need, when user logs in, can do query of userbiz table for userid and store it all in businesses
    __table_args__ = (db.CheckConstraint("email ~ '^[A-Z0-9a-z._%+-]+@[A-Z0-9a-z.-]+\.[A-Za-z]{2,}$'"),)

    biz = db.relationship('Business', secondary='user_biz', backref='users')
    invites = db.relationship('Invite', backref='users')
    friends = (db.relationship('User', secondary='friends',
                               primaryjoin='User.user_id == Friend.user_id',
                               secondaryjoin='User.user_id == Friend.friend_id'))
    promos = db.relationship('Promo', secondary='user_promos', backref='users')
    checkins = db.relationship('CheckIn', backref='users')
    referees = (db.relationship('User', secondary='referrals',
                                primaryjoin='User.user_id == Referral.referer_id',
                                secondaryjoin='User.user_id == Referral.referee_id'))
    reviews = db.relationship('Review', backref='users')

    def __repr__(self):
        """Displays info"""

        return ('<user_id={} username={} email={}>'.format(self.user_id,
                self.username, self.email))
    # TO DO: look into uploading image to flask


class Friend(db.Model):
    """ Relationship information between user profiles. """

    __tablename__ = 'friends'

    link_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        """ Displays info. """

        return ('<user_id={} friend_id={}>'.format(self.user_id, self.friend_id))


class UserBiz(db.Model):
    """ Relationship information between business user profile and related
    businesses that are claimed. """

    __tablename__ = 'user_biz'

    userbiz_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    biz_id = db.Column(db.Integer, db.ForeignKey('businesses.biz_id'))

    def __repr__(self):
        """ Displays info. """

        return ('<user_id={} biz_id={}>'.format(self.user_id, self.biz_id))


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
    url = db.Column(db.String(64), nullable=True)
    category = db.Column(db.String(64), nullable=True)
    days_open = db.Column(db.String(64), nullable=True)
    open_time = db.Column(db.Integer, nullable=True)
    close_time = db.Column(db.Integer, nullable=True)
    claimed = db.Column(db.Boolean, nullable=False, default=False)
    biz_pic = db.Column(db.String(64), nullable=True)
    lat = db.Column(db.String(64), nullable=True)
    lng = db.Column(db.String(64), nullable=True)
    latlng = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    __table_args__ = (db.CheckConstraint("email ~ '^[A-Z0-9a-z._%+-]+@[A-Z0-9a-z.-]+\.[A-Za-z]{2,}$'"),)
    # TO DO: add field for coordinates using postgis library

    checkins = db.relationship('CheckIn', backref='biz')
    referrals = db.relationship('Referral', backref='biz')
    reviews = db.relationship('Review', backref='biz')
    promos = db.relationship('Promo', backref='biz')

    def __repr__(self):
        """ Displays info. """

        return ('<biz_id={} biz_name={}>'.format(self.biz_id, self.biz_name))


class Promo(db.Model):
    """ Promotion model. """

    __tablename__ = 'promos'

    promo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    biz_id = db.Column(db.Integer, db.ForeignKey('businesses.biz_id'))
    title = db.Column(db.String(64), nullable=False)
    descr = db.Column(db.String(64), nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    referral_promo = db.Column(db.Boolean, nullable=False, default=False)
    birthday_promo = db.Column(db.Boolean, nullable=False, default=False)
    redeem_count = db.Column(db.Integer, nullable=False, default=None)

    def __repr__(self):
        """ Displays info. """

        return ('<promo_id={} biz_id={} title={} end_date={}>'
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

        return ('<userpromo_id={} user_id={} promo_id={} redeemed={}>'
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

        return ('<checkin_id={} user_id={} biz_id={} checkin_date={}>'
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

        return ('<referral_id={} biz_id={} refer_date={} userpromo_id>'
                .format(self.referral_id, self.biz_id, self.refer_date, self.userpromo_id))


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

        return ('<review_id={} user_id={} biz_id={} rating={}>'
                .format(self.review_id, self.user_id, self.biz_id, self.rating))


class LikeReview(db.Model):
    """ Tracks user 'likes' of individual reviews by business. """

    __tablename__ = 'likes'

    like_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.review_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        """ Displays info. """

        return ('<review_id={} user_id={}>'.format(self.review_id, self.user_id))


class Invite(db.Model):
    """ User invite model. """

    __tablename__ = 'invites'

    invite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    friend_email = (db.Column(db.String(64), nullable=False))
    accepted = db.Column(db.Boolean, nullable=False, default=False)
    __table_args__ = (db.CheckConstraint("friend_email ~ '^[A-Z0-9a-z._%+-]+@[A-Z0-9a-z.-]+\.[A-Za-z]{2,}$'"),)
    # data modeling lecture, look at many to many demo, instantiate book and user and comment link

    def __repr__(self):
        """ Displays info. """

        return ('<invite_id={} user_id={} accepted={}'
                .format(self.invite_id, self.user_id, self.accepted))

# User.promos = association_proxy('user_promos', "user")
# Promo.users = association_proxy('user_promos', 'promo')


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///buddy'
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
