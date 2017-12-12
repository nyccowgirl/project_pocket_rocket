from __future__ import division
from flask import Flask  # session
from model import connect_to_db, User  # CheckIn, Friend, db, Promo,
# from sqlalchemy.sql import extract
# from degrees import BinarySearchNode as bsn

import sendgrid
import os
from sendgrid.helpers.mail import *

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SHHHHHHIIIITTTT"

# SendGrid for processing emails

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

##############################################################################


def friend_request(friend_email, invite_id):
    """ Generate email with url for registration & linking friends."""

    domain = 'localhost:5000'

    url_string = '/registration/?invite={}'

    url_link = domain + url_string.format(invite_id)

    user = User.query.get(session['user_id'])

    from_email = Email(user.email)
    to_email = Email(friend_email)
    subject = "You've been invited!"
    content = Content('text/plain', "{fname} {lname} has invited you to join the BUDdy community to support local small businesses.\n \
                                    Click on the link to quickly register and become friends with {url}.\n \
                                    {fname}".format(fname=user.first_name, lname=user.last_name, url=url_link))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


def lost_pword(email):
    """ Generate email with url for resetting password. """

    domain = 'localhost:5000'

    url_string = '/pword-reset/?email={}'

    url_link = domain + url_string.format(email)

    user = User.query.filter_by(email=email).first()

    from_email = Email(user.email)
    to_email = Email(user.email)
    subject = "Brain Fart"
    content = Content('text/plain', "We all have momentary lapses.\n \
                                    Click on the link to reset your password: {url}."
                      .format(url=url_link))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


##############################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)
