from flask import Flask, json  # jsonify  # session
from model import User, Friend, connect_to_db  # db
# from sqlalchemy import func
import json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
# app.secret_key = "SHHHHHHIIIITTTT"

##############################################################################


def make_nodes_and_paths(friends_lst):
    """ Create bidirectional graph of friend relationships via Friends table. """

    # nodes = {}

    # for item in friends_lst:
    #     friend1, friend2, group = item
    #     for person in pair:
    #         if not nodes.get(person):
    #             nodes[person] = pair[1]

    # nodes = [{'name': person, 'friend': nodes[person]} for person in nodes.keys()]

    nodes = {}
    for item in friends_lst:
        friend1, friend2, group = item
        if not nodes.get(friend1):
            nodes[friend1] = group
        elif nodes.get(friend1) > group:
            nodes[friend1] = group

    nodes = [{'name': person, 'group': nodes[person]} for person in nodes.keys()]

    index_nodes = {}
    for idx, n in enumerate(nodes):
        index_nodes[n['name']] = (idx, n['group'])

    paths = []

        # paths.append({'source': item[1], 'target': item[0]})

    for item in friends_lst:
        # one = User.query.get(item.user_id)
        # two = User.query.get(item.friend_id)
        source, target, group = item
        paths.append({'source': index_nodes[source][0], 'target': index_nodes[target][0]})

    # print nodes
    # print index_nodes
    # print paths

    return nodes, paths


def see_friends(user_id, max_degree=6):
    """ Provides information on connections.

    Input: person_id, a list of friendships 'in the universe', max degress of
           separation
    Output: a list of tuples of the format: [(friend_id, degrees_of_separation,
            connector)]

    Note: a high-degree connection could have multiple people that connects person
    to 'chain' of friends. In that case, the algorithm would add multiple tuples,
    one for each connector. Users can de-dupe after or modified to de-dupe on the fly.
    """

    friends_lst = set()

    # pull complete friends table
    friends = Friend.query.all()
    raw_connections = set()

    for item in friends:
        raw_connections.add((item.user_id, item.friend_id))

    # add user into friends_lst as group 0
    user = User.query.get(user_id)
    friends_lst.add((user.username, user.username, 0))

    degree = 1

    def inner_recurse(friends_to_check, current_connections, current_degree):
        """ Recursive part of see_friends function."""

        # base cases to the recursion

        if current_degree > max_degree:
            return

        if len(current_connections) == 0:
            return

        if len(friends_to_check) == 0:
            return

        # list of connections to NOT check on next recursion
        connections_to_ignore = set()

        # list of people from previous 'degree'
        new_friends_to_check = set()

        # unused connections to pass to next level
        new_connections = set()

        # loop through all connections and record friendship along with current degree
        for connection in current_connections:
            friend1_id, friend2_id = connection
            friend1 = User.query.get(friend1_id)
            friend2 = User.query.get(friend2_id)
            for friend_to_check in friends_to_check:
                # if the first person listed is one of our recorded friends,
                # then the second person is a 'friend', making this person a
                #connection of whatever degree we're currently in
                if friend_to_check == friend1_id:
                    friends_lst.add((friend2.username, friend1.username, current_degree))
                    new_friends_to_check.add(friend2_id)
                    # already recorded this connection so can skip in the future
                    connections_to_ignore.add(connection)

                #same as above but need to check both since either could be match
                elif friend_to_check == friend2_id:
                    friends_lst.add((friend1.username, friend2.username, current_degree))
                    new_friends_to_check.add(friend1_id)

                    # already recorded this connection so can skip in the future
                    connections_to_ignore.add(connection)

        for connection in current_connections:
            if connection not in connections_to_ignore:
                new_connections.add(connection)

        inner_recurse(new_friends_to_check, new_connections, current_degree + 1)

    # start recursion loops
    inner_recurse({user_id}, raw_connections, degree)

    friends_lst = list(friends_lst)

    return friends_lst


##############################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)
