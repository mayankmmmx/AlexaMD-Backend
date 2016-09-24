# hack for harambe

from random import choice, randint
from pymongo import MongoClient

def respond(get_args):
    match_id = get_args['match_id']
    client = MongoClient()
    db = client.harambe
    questions = db.questions

    match_questions = questions.find_one({'match_id': match_id})
    if match_questions:
        del match_questions['_id']
        return match_questions
    new_questions = {'questions': [q.__dict__ for q in generate_questions(int(get_args['elo']))]}
    new_questions['match_id'] = match_id
    questions.insert_one(new_questions)
    del new_questions['_id']
    return new_questions


def generate_questions(elo=1200):
    questions = []
    # LOL too lazy to make a transformation function so...
    if elo < 1000:
        diff = 0.5
    elif 1000 <= elo < 1400:
        diff = 1.0
    elif 1400 <= elo < 1800:
        diff = 1.5
    elif 1800 <= elo < 2200:
        diff = 2.5
    else:
        diff = 3.5

    for i in range(1, 10):
        # addition problems only, for now
        ans = int(1+diff*randint(2, 10))
        total = int(diff*randint(ans+10, ans*8))
        coeff = total//ans
        constant = total - coeff*ans
        if constant < 2:
            adj = randint(2, 5)
            constant += adj
            total += adj
        raw = "{}x + {} = {}".format(coeff, constant, total)
        english = englishify(coeff, constant, total)
        questions.append(_Question(i, raw, english, ans))
    return questions


def englishify(coeff, constant, total):
    # apparently random choice needs at least 2 elements lol
    templates = ("{} has ${}. After buying {} {}s, {} has ${}. How many dollars did each {} cost?",
                 "{} has ${}. After buying {} {}s, {} has ${}. How many dollars did each {} cost?")
    names = ("Peter", "Josh", "David", "Mayank", "Harambe")
    items = ("apple", "banana", "orange", "pencil", "meme")  # only words with plural -s form
    n, i = choice(names), choice(items)
    return choice(templates).format(n, total, coeff, i, n, constant, i)


class _Question:
    def __init__(self, pid, question_raw, question_english, question_answer):
        self.pid = pid
        self.question_raw = question_raw
        self.question_english = question_english
        self.question_answer = question_answer
