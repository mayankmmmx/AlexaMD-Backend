import requests
import json
import pymysql.cursors

def get_symptom_ids(symptoms):
	symptom_ids = []
	connection = pymysql.connect(
							 host='localhost',
                             user='root',
                             password='',
                             db='alexa_md',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		for symptom in symptoms:
			sql = "SELECT `id` FROM `symptoms` WHERE `symptom`=%s"
			cursor.execute(sql, (symptom))
			result = cursor.fetchone()
			symptom_ids.append(result["id"])
	connection.close()
	return symptom_ids

def create_post_data(symptom_ids):
	evidence = []
	for symptom_id in symptom_ids:
		evidence_blob = {
			"id": symptom_id,
			"choice_id": "present"
		}
		evidence.append(evidence_blob)

	return json.dumps({
		"sex": "male",
		"age": "29",
		"evidence": evidence
	})

def get_diagnoses(evidence):
	POST_URL = "https://api.infermedica.com/v2/diagnosis"
	header = { "app_id" : "9cfcafae", "app_key" : "55b78a933718c8e68ba37f2f8d80b1a7", "Content-Type": "application/json"}
	response = requests.post(POST_URL, headers=header, data=evidence)
	diagnoses = response.json().get("conditions")

	if len(diagnoses) is 0:
		return "Sorry, I'm not too sure what's wrong. Visit a doctor for a better diagnosis"
	elif len(diagnoses) == 1:
		return "You most likely have " + diagnoses[0].get("name") + ". However, you should visit a doctor for more accurate results."
	else:
		most_likely = diagnoses[0]
		second_most_likely = diagnoses[1]
		return "You most likely have " + most_likely.get("name") + " or " + second_most_likely.get("name") +". However, you should visit a doctor for more accurate results."


	print(len(diagnoses))

def respond(data):
	symptom_ids = get_symptom_ids(data.get("symptoms"))
	diagnosis = get_diagnoses(create_post_data(symptom_ids))

	return {
		'status': 0,
		'diagnosis': diagnosis
	}
