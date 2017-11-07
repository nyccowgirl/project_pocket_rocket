from model import connect_to_db, db, User, Business

def check_user_info(user_input):
    """Check user input of either username or email against database."""

    user = User.query.filter(User.username == user_input | User.email == user_input).first()

    return user
    