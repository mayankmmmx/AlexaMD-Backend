import requests

POST_URL = "http://localhost:5000/harambe/create_account"
POST_DATA = {
    'username': input("username: ").strip(),
    'password': input("password: ").strip(),
}

r = requests.post(POST_URL, json=POST_DATA)
print(r.text)
