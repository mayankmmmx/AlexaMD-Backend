import requests

POST_URL = "http://localhost:5000/harambe/submit_match"
POST_DATA = {
    'match_id': 'sdfdfgfdgdf',
    'draw': input("draw (no/yes): ").strip(),
    'winner': input("winner username: ").strip(),
    'loser': input("loser username: ").strip()
}

r = requests.post(POST_URL, json=POST_DATA)
print(r.text)
