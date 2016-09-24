# hack for harambe
from pymongo import MongoClient
ELO_K_FACTOR = 100


def adjust_elo(r1, r2, winner):
    # r1, r2 are elo ratings
    # winner = 1 if player 1 wins, 0.5 if draw, 0 if player 2 wins
    s1, s2, a_r1, a_r2 = winner, 1 - winner, pow(10, r1/400), pow(10, r2/400)
    e1, e2 = a_r1 / (a_r1 + a_r2), a_r2 / (a_r1 + a_r2)
    return int(r1 + ELO_K_FACTOR * (s1 - e1)), int(r2 + ELO_K_FACTOR * (s2 - e2))


def respond(data):
    p_one_id = data.get('p_one_id')
    p_two_id = data.get('p_two_id')

    client = MongoClient()
    db = client.harambe
    users = db.users

    winner_old_elo = int(users.find_one({'username': p_one_id}).get('elo'))
    winner_new_elo = winner_old_elo + 31
    loser_old_elo = int(users.find_one({'username': p_two_id}).get('elo'))
    loser_new_elo = loser_old_elo - 31

    return {
        'winner_old_elo': winner_old_elo,
        'winner_new_elo': winner_new_elo,
        'loser_old_elo': loser_old_elo,
        'loser_new_elo': loser_new_elo
    }

def process_match_result(draw, winner, loser):
    client = MongoClient()
    db = client.harambe
    users = db.users
    print ('here2')
    print(winner)
    print(loser)
    if draw:
        match_status = 0.5
    else:
        match_status = 1
    winner_old_elo = int(users.find_one({'username': winner}).get('elo'))
    loser_old_elo = int(users.find_one({'username': loser}).get('elo'))

    winner_new_elo, loser_new_elo = adjust_elo(winner_old_elo, loser_old_elo, match_status)
    if draw:
        users.update_one({'username': winner},
            {'$set': {'elo': winner_new_elo, 'old_elo': winner_old_elo}})
        users.update_one({'username': loser},
            {'$set': {'elo': loser_new_elo, 'old_elo': loser_old_elo}})
    else:  # lol this code is so bad
        users.update_one({'username': winner},
            {'$set': {'elo': winner_new_elo, 'old_elo': winner_old_elo}, '$inc': {'wins': 1}})
        users.update_one({'username': loser},
            {'$set': {'elo': loser_new_elo, 'old_elo': loser_old_elo}, '$inc': {'losses': 1}})
