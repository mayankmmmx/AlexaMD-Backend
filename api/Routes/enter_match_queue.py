# hack for harambe
from pymongo import MongoClient
from random import randint


def respond(data):
    username = data.get('username')

    client = MongoClient()
    db = client.harambe
    queue = db.queue

    queued_match = queue.find_one()
    if queued_match:
        match_id = queued_match['match_id']
        queued_match['p_two_id'] = username
        start_match(queued_match, db)
        queue.remove()
        return {'start_match': 1, 'match_id': match_id}
    else:
        match_id = str(randint(10**12, 10**13 - 1))
        queue.insert_one({'match_id': match_id, 'p_one_id': username})
        return {'start_match': 0, 'match_id': match_id}


def start_match(match, db):
    match_status = {
        'cur_question': 1,
        'p_one_status': 0,
        'p_two_status': 0,
        'p_one_score': 0,
        'p_two_score': 0
    }
    match.update(match_status)
    db.active_matches.insert_one(match)
