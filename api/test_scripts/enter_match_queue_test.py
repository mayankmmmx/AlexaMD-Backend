import requests

POST_URL = "http://localhost:5000/harambe/enter_match_queue"
POST_DATA = {
    'username': input("username: ").strip()
}

r = requests.post(POST_URL, json=POST_DATA)
print(r.text)
