# hack for harambe
from pymongo import MongoClient
from Routes import submit_match

def respond(data):
    username = data.get('username')
    match_id = data.get('match_id')
    status = data.get('status')

    client = MongoClient()
    db = client.harambe
    active_matches = db.active_matches
    if match_id:
        match = active_matches.find_one({'match_id': match_id})
        if not match:
            return {'status': 0}
        if match['cur_question'] == 6:
   	    print('here1')
            if match['p_one_score'] > match['p_two_score']:
                submit_match.process_match_results(0, match['p_one_id'], match['p_two_id'])
            elif match['p_one_score'] < match['p_two_score']:
                submit_match.process_match_results(0, match['p_two_id'], match['p_one_id'])
            else:
                submit_match.process_match_results(1, match['p_one_id'], match['p_two_id'])

        if username and status:
            status = int(status)
            # -1 means locked in with wrong answer or time out
            if match['p_one_id'] == username and match['p_one_status'] != -1:
                match['p_one_status'] = status
            elif match['p_two_id'] == username and match['p_two_status'] != -1:
                match['p_two_status'] = status

        # Check if both players have either failed, timed out
        if match['p_one_status'] == -1 and match['p_two_status'] == -1:
            next_question(match)
        if match['p_one_status'] == 1:
            match['p_one_score'] += 1
            next_question(match)
        if match['p_two_status'] == 1:
            match['p_two_score'] += 1
            next_question(match)

        active_matches.update_one({'match_id': match_id}, {"$set": match})
        # Need to do this because cannot return mongodb _id object
        del match['_id']
        match['status'] = 1
        return match
    return {'status': 0}


def next_question(match):
    match['cur_question'] += 1
    match['p_one_status'] = 0
    match['p_two_status'] = 0

