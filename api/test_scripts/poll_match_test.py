import requests

POST_URL = "http://localhost:5000/harambe/poll_match"
POST_DATA = {
    'username': input("username: ").strip(),
    'match_id': input("match_id: ").strip(),
    'status': input("status: ").strip()
}

r = requests.post(POST_URL, json=POST_DATA)
print(r.text)
