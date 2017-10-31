
import os
import sys
import requests
from urllib import quote
from urllib2 import HTTPError
# import json
import argparse
import pprint

# API constants that won't change
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
# TOKEN_PATH = '/oauth2/token'
# GRANT_TYPE = 'client_credentials'

TOKEN = os.environ['YELP_ACCESS_TOKEN']

# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'


def request(path, payload=None):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        access_token (str): OAuth bearer token, obtained from secrets.sh file.
        payload (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """

    url = API_HOST + quote(path.encode('utf8'))  # quote() from urllib

    header = {
        'Authorization': 'Bearer {}'.format(TOKEN),
    }

    # payload = {
    #     # input other parameters (e.g., location)
    # }

    response = requests.get(url, headers=header, params=payload)

    return response.json()


def get_search_term():
    """Get user input for search term(s), location, and/or search limits.

    Returns:
        term (str): The search term to pass to API.
        location (str): The search location to pass to API.
    """

    print('\nInput any specific search term, location or limit [return if n/a].\n')
    term = raw_input("Search: ")
    location = raw_input("Location: ")
    search_limit = raw_input("Limit: ")

    if search_limit.isdigit():
        search_limit = int(search_limit)

    return term, location, search_limit


def search(term, location, search_limit):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    payload = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': search_limit
    }

    return request(SEARCH_PATH, payload)


def get_business(business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """

    business_path = BUSINESS_PATH + business_id

    return request(business_path)


def get_reviews(business_id):
    """Query the Reviews API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """

    reviews_path = BUSINESS_PATH + business_id + '/reviews'

    return request(reviews_path)


def query_api(term, location, search_limit):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """

    response = search(term, location, search_limit)

    businesses = response.get('businesses')

    if not businesses:
        print(u'\nNo businesses for {} in {} found.\n'.format(term, location))
        return

    business_id = businesses[0]['id']

    print(u'\n{} businesses found, querying business info for the top result "{}" ...\n'.
          format(len(businesses), business_id))

    biz_response = get_business(business_id)

    print(u'\nResult for business "{}" found:\n'.format(business_id))

    pprint.pprint(biz_response, indent=2)

    reviews_response = get_reviews(business_id)

    print(u'\nReviews for business "{}" found:\n'.format(business_id))

    pprint.pprint(reviews_response, indent=2)


def main():
    """ From https://github.com/Yelp/yelp-fusion/tree/master/fusion/python:
    to run for errors.
    """

    term, location, search_limit = get_search_term()

    if search_limit == "":
        search_limit = 10

    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=term,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=location, type=str,
                        help='Search location (default: %(default)s)')
    parser.add_argument('-n', '--limit', dest='search_limit',
                        default=search_limit, type=int,
                        help='Search limit (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location, input_values.search_limit)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {} on {}:\n {}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()
