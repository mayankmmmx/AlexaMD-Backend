import requests

POST_URL = "http://localhost:5000/harambe/diagnosis"
POST_DATA = {
	'sex': 'male',
	'age': '15',
    'symptoms' : ['joint pain', "bad cough"]
}

r = requests.post(POST_URL, json=POST_DATA)
print(r.text)