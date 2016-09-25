import requests

POST_URL = "http://localhost:5000/harambe/diagnosis"
POST_DATA = {
    'symptoms' : ['wheezing', 'seizures', 'fever', 'heartburn']
}

r = requests.post(POST_URL, json=POST_DATA)
print(r.text)