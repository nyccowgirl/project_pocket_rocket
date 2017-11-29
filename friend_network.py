from flask import Flask, jsonify  # session
from model import User, Friend, db, connect_to_db
from sqlalchemy import func
import json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SHHHHHHIIIITTTT"

##############################################################################

def make_nodes_and_paths():
    """ Create bidirectional graph of friend relationships via Friends table. """

    friends = Friend.query.all()

    nodes = {}

    for pair in friends:
        for person in pair:
            person = person.username
            if not nodes.get(person):
                nodes[person] = pair[1].username

    nodes = [{'name': person, 'friend': nodes[person]} for person in nodes.keys()]

    index_nodes = {}
    for idx, n in enumerate(nodes):
        index_nodes[n['name']] = (idx, n['friend'])

    paths = []

    for pair in friends:
        source, target = pair
        paths.append({'source': index_nodes[source][0], 'target': index_nodes[target][0]})

    return nodes, paths
