# hack for harambe
import random
import string
from pymongo import MongoClient

AUTH_TOKEN_LENGTH = 30


def respond(data):
    username = data.get('username')
    password = data.get('password')

    client = MongoClient()
    db = client.harambe
    users = db.users

    if not (username and password):
        return {
            'status': 1,
            'message': 'Username and password required.',
            'auth_token': ''
        }
    if users.find({'username': username}).count():
        return {
            'status': 1,
            'message': 'Username already taken.',
            'auth_token': ''
        }

    new_user_auth = create_auth_token()
    new_user = {
        'username': username,
        'password': password,
        'auth_token': new_user_auth,
        'title': 'Novice',
        'elo': 1200,
        'wins': 0,
        'losses': 0
    }
    users.insert_one(new_user)
    return {
        'status': 0,
        'message': 'Account created successfully!',
        'auth_token': new_user_auth
    }


def create_auth_token():
    auth_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(AUTH_TOKEN_LENGTH))
    return auth_token
