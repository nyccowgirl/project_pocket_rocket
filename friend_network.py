from flask import Flask  # jsonify  # session
from model import User, Friend, connect_to_db  # db
# from sqlalchemy import func
# import json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
# app.secret_key = "SHHHHHHIIIITTTT"

##############################################################################


def make_nodes_and_paths():
    """ Create bidirectional graph of friend relationships via Friends table. """

    friends = Friend.query.all()

    nodes = {}

    for item in friends:
        one = User.query.get(item.user_id)
        two = User.query.get(item.friend_id)
        pair = [one.username, two.username]
        for person in pair:
            if not nodes.get(person):
                nodes[person] = pair[1]

    nodes = [{'name': person, 'friend': nodes[person]} for person in nodes.keys()]

    index_nodes = {}
    for idx, n in enumerate(nodes):
        index_nodes[n['name']] = (idx, n['friend'])

    paths = []

    for item in friends:
        one = User.query.get(item.user_id)
        two = User.query.get(item.friend_id)
        pair = [one.username, two.username]
        source, target = pair
        paths.append({'source': index_nodes[source][0], 'target': index_nodes[target][0]})

    return nodes, paths

def six_degrees(user_id, degree=6):
    """ Create bidirectional graph for a specific user based on a specified
    degree of separation, with default of 6."""

    person = User.query.get(user_id)

    head = person.username

    count = 0
    network = set()
    queue = set()
    seen = set()

    while count <= degree:
        count += 1
        for friend in person.friends:
            network.add((person.username, friend.username, 'group ' + str(count)))
            queue.add(friend.user_id)
            seen.add(user.user_id)
        queue_len = len(queue)





##############################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)
