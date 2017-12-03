# from __future__ import division
from flask import Flask, json  # session
from model import CheckIn, Referral, Promo, Business, db, connect_to_db  # Promo
# from sqlalchemy.sql import extract
# from degrees import BinarySearchNode as bsn
from sqlalchemy import func
# import json

app = Flask(__name__)


##############################################################################


def bubble_data_refs():
    """Creates and jsonify dataset for bubble chart based on referrals. Writes
    data to file and returns nothing."""

    biz_dict = {}

    # Query of all businesses to put biz_id as key in dictionary
    biz = Business.query.all()

    for item in biz:
        biz_dict[item.biz_id] = {'name': item.biz_name, 'category': item.category, 'tot_checkins': None, 'tot_refs': None, 'tot_reds': None}

    # Query all checkins and updates total checkins by biz_id

    checkins = (db.session.query(CheckIn.biz_id, func.count(CheckIn.biz_id)).group_by(CheckIn.biz_id).order_by(CheckIn.biz_id).all())

    for item in checkins:
        biz_dict[item[0]]['tot_checkins'] = item[1]

    # Query all referrals and updates total referrals by biz_id

    referrals = (db.session.query(Referral.biz_id, func.count(Referral.biz_id)).group_by(Referral.biz_id).order_by(Referral.biz_id).all())

    for item in referrals:
        biz_dict[item[0]]['tot_refs'] = item[1]

    #Query all redemptions and updates total redemptions by biz_id

    redemptions = (db.session.query(Promo.biz_id, func.sum(Promo.redeem_count)).group_by(Promo.biz_id).order_by(Promo.biz_id).all())

    for item in redemptions:
        biz_dict[item[0]]['tot_reds'] = item[1]

    # Create dictionary with key of categories and various data fields needed for bubble graph.

    cat_dict = {'Bar': ['total1', 'older1', 'perc1', 'tag1'], 'Cleaners': ['total2', 'older2', 'perc2', 'tag2'], 'Coffee/Cafe/Tea': ['total3', 'older3', 'perc3', 'tag3'], 'Deli/Grocery': ['total4', 'older4', 'perc4', 'tag4'], 'Florist': ['total5', 'older5', 'perc5', 'tag5'], 'Home Services': ['total6', 'older6', 'perc6', 'tag6'], 'Medical Services': ['total7', 'older7', 'perc7', 'tag7'], 'Legal Services': ['total8', 'older8', 'perc8', 'tag8'], 'Nightlife': ['total9', 'older9', 'perc9', 'tag9'], 'Pets': ['total10', 'older10', 'perc10', 'tag10'], 'Restaurant': ['total11', 'older11', 'perc11', 'tag11'], 'Salon': ['total12', 'older12', 'perc12', 'tag12'], 'Spa': ['total13', 'older13', 'perc13', 'tag13']}
    # cat_dict = {'bar': ['total1', 'older1', 'perc1', 'tag1'], 'cleaner': ['total2', 'older2', 'perc2', 'tag2'], 'cafe': ['total3', 'older3', 'perc3', 'tag3'], 'grocery': ['total4', 'older4', 'perc4', 'tag4'], 'florist': ['total5', 'older5', 'perc5', 'tag5'], 'home': ['total6', 'older6', 'perc6', 'tag6'], 'medicine': ['total7', 'older7', 'perc7', 'tag7'], 'legal': ['total8', 'older8', 'perc8', 'tag8'], 'nightlife': ['total9', 'older9', 'perc9', 'tag9'], 'pet': ['total10', 'older10', 'perc10', 'tag10'], 'restaurant': ['total11', 'older11', 'perc11', 'tag11'], 'salon': ['total12', 'older12', 'perc12', 'tag12'], 'spa': ['total13', 'older13', 'perc13', 'tag13']}

    # Sort dictionary by descending older based on total checkins and then total referrals, using keys in a list

    rank_lst = sorted(biz_dict.keys(), key=lambda x: (biz_dict[x]['tot_checkins'], biz_dict[x]['tot_refs']))

    # Gather data for top 100 businesses

    top_rank = rank_lst[:200]

    # Create list of individual dictionary of each business data

    datasource = []

    for item in top_rank:
        datasource.append({cat_dict[biz_dict[item]['category']][0]: biz_dict[item]['tot_checkins'], cat_dict[biz_dict[item]['category']][1]: biz_dict[item]['tot_refs'], cat_dict[biz_dict[item]['category']][2]: biz_dict[item]['tot_reds'], cat_dict[biz_dict[item]['category']][3]: biz_dict[item]['name']})

    with open('static/js/bubble_data_refs.js', 'w') as outfile:
        json.dump(datasource, outfile, indent=2)

    with open('static/js/bubble_data_refs.js', 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('let dataSourceRefs = ' + content)

    with open('static/js/bubble_data_refs.js', 'a') as f:
        f.write(';')

def bubble_data_promos():
    """Creates and jsonify datasets for bubble chart based on promotions. Writes
    data to file and returns nothing."""

    biz_dict = {}

    # Query of all businesses to put biz_id as key in dictionary
    biz = Business.query.all()

    for item in biz:
        biz_dict[item.biz_id] = {'name': item.biz_name, 'category': item.category, 'tot_checkins': None, 'tot_promos': None, 'tot_reds': None}

    # Query all checkins and updates total checkins by biz_id

    checkins = (db.session.query(CheckIn.biz_id, func.count(CheckIn.biz_id)).group_by(CheckIn.biz_id).order_by(CheckIn.biz_id).all())

    for item in checkins:
        biz_dict[item[0]]['tot_checkins'] = item[1]

    # Query all referrals and updates total referrals by biz_id

    promotions = (db.session.query(Promo.biz_id, func.count(Promo.biz_id)).group_by(Promo.biz_id).order_by(Promo.biz_id).all())

    for item in promotions:
        biz_dict[item[0]]['tot_promos'] = item[1]

    #Query all redemptions and updates total redemptions by biz_id

    redemptions = (db.session.query(Promo.biz_id, func.sum(Promo.redeem_count)).group_by(Promo.biz_id).order_by(Promo.biz_id).all())

    for item in redemptions:
        biz_dict[item[0]]['tot_reds'] = item[1]

    # Create dictionary with key of categories and various data fields needed for bubble graph.

    cat_dict = {'Bar': ['total1', 'older1', 'perc1', 'tag1'], 'Cleaners': ['total2', 'older2', 'perc2', 'tag2'], 'Coffee/Cafe/Tea': ['total3', 'older3', 'perc3', 'tag3'], 'Deli/Grocery': ['total4', 'older4', 'perc4', 'tag4'], 'Florist': ['total5', 'older5', 'perc5', 'tag5'], 'Home Services': ['total6', 'older6', 'perc6', 'tag6'], 'Medical Services': ['total7', 'older7', 'perc7', 'tag7'], 'Legal Services': ['total8', 'older8', 'perc8', 'tag8'], 'Nightlife': ['total9', 'older9', 'perc9', 'tag9'], 'Pets': ['total10', 'older10', 'perc10', 'tag10'], 'Restaurant': ['total11', 'older11', 'perc11', 'tag11'], 'Salon': ['total12', 'older12', 'perc12', 'tag12'], 'Spa': ['total13', 'older13', 'perc13', 'tag13']}
    # cat_dict = {'bar': ['total1', 'older1', 'perc1', 'tag1'], 'cleaner': ['total2', 'older2', 'perc2', 'tag2'], 'cafe': ['total3', 'older3', 'perc3', 'tag3'], 'grocery': ['total4', 'older4', 'perc4', 'tag4'], 'florist': ['total5', 'older5', 'perc5', 'tag5'], 'home': ['total6', 'older6', 'perc6', 'tag6'], 'medicine': ['total7', 'older7', 'perc7', 'tag7'], 'legal': ['total8', 'older8', 'perc8', 'tag8'], 'nightlife': ['total9', 'older9', 'perc9', 'tag9'], 'pet': ['total10', 'older10', 'perc10', 'tag10'], 'restaurant': ['total11', 'older11', 'perc11', 'tag11'], 'salon': ['total12', 'older12', 'perc12', 'tag12'], 'spa': ['total13', 'older13', 'perc13', 'tag13']}

    # Sort dictionary by descending older based on total checkins and then total referrals, using keys in a list

    rank_lst = sorted(biz_dict.keys(), key=lambda x: (biz_dict[x]['tot_checkins'], biz_dict[x]['tot_promos']))

    # Gather data for top 100 businesses

    top_rank = rank_lst[:200]

    # Create list of individual dictionary of each business data

    datasource = []

    for item in top_rank:
        datasource.append({cat_dict[biz_dict[item]['category']][0]: biz_dict[item]['tot_checkins'], cat_dict[biz_dict[item]['category']][1]: biz_dict[item]['tot_promos'], cat_dict[biz_dict[item]['category']][2]: biz_dict[item]['tot_reds'], cat_dict[biz_dict[item]['category']][3]: biz_dict[item]['name']})

    with open('static/js/bubble_data_promos.js', 'w') as outfile:
        json.dump(datasource, outfile, indent=2)

    with open('static/js/bubble_data_promos.js', 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('let dataSourcePromos = ' + content)

    with open('static/js/bubble_data_promos.js', 'a') as f:
        f.write(';')


##############################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)
    # bubble_data()
