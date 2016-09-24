# hack for harambe
from pymongo import MongoClient
import pymongo


def respond(data):
    username = data.get('username')

    client = MongoClient()
    db = client.harambe
    users = db.users

    user_info = users.find_one({'username': username})

    all_users = users.find()
    num_higher = all_users.count()
    if user_info:
        for x in all_users:
            # Need to check the keys for legacy reasons
            if 'elo' in x and 'elo' in user_info and x['elo'] <= user_info['elo']:
                num_higher -= 1

    all_users_sorted = list(users.find().sort('elo',
                            pymongo.DESCENDING).limit(10))
    all_users_sorted = [{'username': x['username'], 'elo': x['elo']} for x in all_users_sorted]

    return {'top_users': all_users_sorted, 'user_rank': num_higher}
