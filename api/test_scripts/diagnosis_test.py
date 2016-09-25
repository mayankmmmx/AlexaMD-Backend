import requests

POST_URL = "http://localhost:5000/harambe/diagnosis"
POST_DATA = {
	'sex': 'male',
	'age': '12',
    'symptoms' : ["i think i have joint pain"]
}

r = requests.post(POST_URL, json=POST_DATA)
print(r.text)