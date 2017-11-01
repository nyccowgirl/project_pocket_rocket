from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_imageattach.entity import Image, image_attachment


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
    user_pic = image_attachment('UserPic')
    dob = db.Column(db.DateTime, nullable=True)
    join_date = db.Column(db.DateTime, nullable=False)
    biz_acct = db.Column(db.Boolean, nullable=False, default=False)

    userpic = db.relationship('UserPic')
    biz = db.relationship('Business', secondary='user_biz')
    friends = db.relationship('User', seondary='friends')
    promos = db.relationship('Promo', secondary='user_promos')
    checkins = db.relationship('CheckIn')
    referrals = db.relationship('Referral')
    reviews = db.relationship('Review')
    invites = db.relationship('Invite')
    # not sure if this is done correctly with the secondary and both users from
    # friends table relying on foreign key from users table

    def __repr__(self):
        """Displays info"""

        return ("<user_id={} username={} email={}>".format(self.user_id,
                self.username, self.email))


class UserPic(db.Model, Image):  # need to check on the image one (https://sqlalchemy-imageattach.readthedocs.io/en/1.1.0/guide/declare.html)
    """ User picture model. """

    __tablename__ = 'user_pics'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)

    user = db.relationship('User', uselist=False)


class Friend(db.Model):
    """ Relationship information between user profiles. """

    __tablename__ = 'friends'

    # Links user account to friends.
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship('User')

    def __repr__(self):
        """ Displays info. """

        return ("<user_id={} friend_id={}>".format(self.user_id, self.friend_id))


class UserBiz(db.Model):
    """ Relationship information between business user profile and related
    businesses that are claimed. """

    __tablename__ = 'user_biz'

    # Links business user account (users.biz_acct = True) to related business(es) claimed.
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    biz_id = db.Column(db.Integer, db.ForeignKey('businesses.biz_id'))

    user = db.relationship('User')
    biz = db.relationship('Business')

    def __repr__(self):
        """ Displays info. """

        return ("<user_id={} biz_id={}>".format(self.user_id, self.biz_id))


class Business(db.Model):
    """ Business model. """

    __tablename__ = 'businesses'

    biz_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    biz_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(64), nullable=True)
    state = db.Column(db.String(64), nullable=True)
    country = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    valid_email = db.Column(db.Boolean, nullable=False, default=False)
    category = db.Column(db.String(64), nullable=True)
    days_open = db.Column(db.String(64), nullable=True)
    open_time = db.Column(db.Integer, nullable=True)
    close_time = db.Column(db.Integer, nullable=True)
    claimed = db.Column(db.Boolean, nullable=False, default=False)
    biz_pic_main = image_attachment('BizPic')
    # biz_pic_other = image_attachment() # maybe future versions to determine how to do gallery of pics

    users = db.relationship('User', secondary='user-biz')
    checkins = db.relationship('CheckIn')
    referrals = db.relationship('Referral')
    reviews = db.relationship('Review')

    def __repr__(self):
        """ Displays info. """

        return ("<biz_id={} bizname={}>".format(self.biz_id, self.bizname))


class BizPic(db.Model, Image):  # need to check on the image one (https://sqlalchemy-imageattach.readthedocs.io/en/1.1.0/guide/declare.html)
    """ Business picture model. """

    __tablename__ = 'biz_pics'

    biz_id = db.Column(db.Integer, db.ForeignKey('businesses.biz_id'), primary_key=True)

    biz = db.relationship('Business', uselist=False)


class BizPromo(db.Model):
    """ Relationship information between business(es) and related promotions. """

    __tablename__ = 'biz_promos'

    biz_id = db.Column(db.Integer, db.ForeignKey('businesses.biz_id'), primary_key=True)
    promo_id = db.Column(db.Integer, db.ForeignKey('promos.promo_id'))
    promo_active = db.Column(db.Boolean, nullable=False, default=True)

    biz = db.relationship('Business')
    promos = db.relationship('Promo')

    def __repr__(self):
        """ Displays info. """

        return ("<biz_id={} promo_id={} promo_active={}>".format(self.biz_id,
                                                                 self.promo_id,
                                                                 self.promo_active))


class Promo(db.Model):
    """ Promotion model. """

    __tablename__ = 'promos'

    promo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    descr = db.Column(db.String(64), nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    referral_promo = db.Column(db.Boolean, nullable=False, default=False)
    birthday_promo = db.Column(db.Boolean, nullable=False, default=False)
    redeem_count = db.Column(db.Integer, nullable=False, default=None)

    users = db.relationship('User', secondary='user_promos')
    biz = db.relationship('Business')

    def __repr__(self):
        """ Displays info. """

        return ("<promo_id={} title={} end_date={}>".format(self.promo_id,
                                                            self.title,
                                                            self.end_date))


class UserPromo(db.Model):
    """ Relationship information between user and related promotions. """

    __tablename__ = 'user_promos'

    user_promo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    promo_id = db.Column(db.Integer, db.ForeignKey('promos.promo_id'))
    redeem_date = db.Column(db.DateTime, nullable=True)
    redeemed = db.Column(db.Boolean, nullable=False, default=False)

    users = db.relationship('User')
    promos = db.relationship('Promo')

    def __repr__(self):
        """ Displays info. """

        return ("<user_promo_id={} user_id={} promo_id={} redeemed={}>"
                .format(self.user_promo_id, self.user_id, self.promo_id, self.redeemed))


class CheckIn(db.Model):
    """ Check-in model. """

    __tablename__ = 'check_ins'

    checkin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    biz_id = db.Column(db.Integer, db.ForeignKey('businesses.biz_id'))
    checkin_date = db.Column(db.DateTime, nullable=False)

    users = db.relationship('User')
    biz = db.relationship('Business')

    def __repr__(self):
        """ Displays info. """

        return ("<checkin_id={} user_id={} biz_id={} checkin_date={}>"
                .format(self.checkin_id, self.user_id, self.biz_id, self.checkin_date))


class Referral(db.Model):
    """ Referral model. """

    __tablename__ = 'referrals'

    referral_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    referree_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    biz_id = db.Column(db.Integer, db.ForeignKey('businesses.biz_id'))
    refer_date = db.Column(db.DateTime, nullable=False)

    users = db.relationship('User')
    biz = db.relationship('Business')

    def __repr__(self):
        """ Displays info. """

        return ("<referral_id={} biz_id={} refer_date={} redeem_date>"
                .format(self.referral_id, self.biz_id, self.refer_date, self.redeem_date))


class Review(db.Model):
    """ Review model. """

    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    biz_id = db.Column(db.Integer, db.ForeignKey('businesses.biz_id'))
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(5000), nullable=False)
    like = db.Column(db.Integer, nullable=False, default=0)
    # use to count likes of review
    dispute = db.Column(db.Boolean, nullable=False, default=False)
    response = db.Column(db.String(5000), nullable=True)
    revise_review = db.Column(db.Boolean, nullable=False, default=False)
    new_rating = db.Column(db.Integer, nullable=True)
    new_review = db.Column(db.String(3000), nullable=True)

    user = db.relationship('User')
    biz = db.relationship('Business')

    def __repr__(self):
        """ Displays info. """

        return ("<review_id={} user_id={} biz_id={} rating={}>"
                .format(self.review_id, self.user_id, self.biz_id, self.rating))


class Invite(db.Model):
    """ User invite model. """

    __tablename__ = 'invites'

    invite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('users.user_id'), nullable=False)
    friend_email = db.Column(db.String(64), nullable=False)
    accepted = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship('User')

    def __repr__(self):
    """ Displays info. """

        return ("<invite_id={} user_id={} accepted={}"
                .format(self.invite_id, self.user_id, self.accepted))


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
