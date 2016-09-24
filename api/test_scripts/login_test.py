import requests

GET_BASE_URL = "http://localhost:5000/harambe/login"
GET_URL = GET_BASE_URL + "?username={}&password={}".format(
    input("login username: ").strip(), input("login password: ").strip())

r = requests.get(GET_URL)
print(r.text)
