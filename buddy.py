from model import User  # connect_to_db, db, Business


def check_user_info(user_input):
    """
    Check user input of either username or email against database.

    TO DO: Build out doctests
    """

    user = User.query.filter(User.username == user_input | User.email == user_input).first()

    return user


def calc_game(user_obj):
    """
    Calculate various metrics (e.g., total check-ins, total referrals and
    respective redemptions, total reviews, etc.) for gamification component.

    TO DO: Build out doctests
    """
