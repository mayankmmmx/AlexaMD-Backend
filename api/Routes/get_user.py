# hack for harambe
from pymongo import MongoClient


def respond(get_args):
    username = get_args['username']

    client = MongoClient()
    db = client.harambe
    users = db.users

    user_info = users.find_one({'username': username})
    if not user_info:
        return {}
    return {
        'username': user_info['username'],
        'title': user_info['title'],
        'elo': user_info['elo'],
        'wins': user_info['wins'],
        'losses': user_info['losses']
    }
