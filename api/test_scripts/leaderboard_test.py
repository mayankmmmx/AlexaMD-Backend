import requests

GET_BASE_URL = "http://localhost:5000/harambe/get_leaderboard"
GET_URL = GET_BASE_URL + "?username={}".format(
    input("login username: ").strip())

r = requests.get(GET_URL)
print(r.text)
