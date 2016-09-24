# hack for harambe
from pymongo import MongoClient

AUTH_TOKEN_LENGTH = 30


def respond(get_args):
    username = get_args['username']
    password = get_args['password']

    client = MongoClient()
    db = client.harambe
    users = db.users

    user_pass_match = users.find_one({'username': username, 'password': password})
    if user_pass_match:
        user_auth = user_pass_match['auth_token']
        return {
            'status': 0,
            'message': 'Login successful!',
            'auth_token': user_auth
        }
    return {
        'status': 1,
        'message': 'Invalid username or password.',
        'auth_token': ''
    }
