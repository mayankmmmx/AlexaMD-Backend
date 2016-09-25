import requests

POST_URL = "http://localhost:5000/harambe/diagnosis"
POST_DATA = {
    'symptoms' : ['harambe', 'is', 'our', 'god']
}

r = requests.post(POST_URL, json=POST_DATA)
print(r.text)