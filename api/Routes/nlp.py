from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import pymysql.cursors

filler_words = stopwords.words('english')
filler_words.append('think')
st = LancasterStemmer()

verbs = [
	"hurt",
	"pain",
	"itch",
	"burn",
	"agitat",
	"spasm",
	"accelerat",
	"aggrevat",
	"sweat",
	"attack",
	"chang",
	"drink",
	"feel",
	"swell",
	"itch",	
	"ach",
	"vomit",
	"hear",
	"cough",
]

body_parts = [
	"abdomin",
	"nose",
	"ear",
	"eye",
	"feet",
	"teeth",
	"leg",
	"throat",
	"chest",
	"heart",
	"lung",
	"back",
	"head",
	"finger",
	"toe",
	"anus",
	"knees",
	"waist",
	"thigh",
	"tongue",
	"neck",
	"shoulder",
	"joint",
	"mouth",
	"blood",

]

body_part_association = {
	"teeth":"tooth",
	"tooth":"teeth",
	"feet":"foot",
	"foot":"feet",
}

body_parts_conversion = {
	"stomach": "abdominal",
	"tummy": "abdominal",
	"poop": "stools",
	"butt":"anus",
	"pee":"urin",
	"threw":"vomit",
	"sore":"itch",
}

def decode(phrase, data): 
	word_list = phrase.split(" ")
	filtered_words = [word for word in word_list if word not in filler_words]
	temp = " ".join(filtered_words)
	if temp in data.keys():
		return data[temp]

	for index in range(len(filtered_words)):
		if filtered_words[index] in body_parts_conversion.keys():
			filtered_words[index] = body_parts_conversion[filtered_words[index]]
		if filtered_words[index] not in body_parts:
			filtered_words[index] = st.stem(filtered_words[index])

	phrase_verbs = []
	phrase_body_parts = []

	for word in filtered_words:
		if word in verbs:
			phrase_verbs.append(word)
		elif word in body_parts:
			phrase_body_parts.append(word)
			if word in body_part_association.keys():
				phrase_body_parts.append(body_part_association[word])

	related = []

	for body_part in phrase_body_parts:
		for symptom in data.keys():
			if body_part in symptom:
				related.append(symptom)

	if len(related) > 0:
		temp = []
		for symptom in related:
			for verb in phrase_verbs:
				if verb in symptom:
					temp.append(symptom)

		if len(temp) is 0:
			for symptom in related:
				for verb in verbs:
					if verb in symptom:
						temp.append(symptom)
		
		if len(temp) is not 0:
			related = temp

	if len(related) is 0:
		for verb in phrase_verbs:
			for symptom in data.keys():
				if verb in symptom:
					related.append(symptom)
	
	if len(related) is 0:
		return ""
	else:
		return data[related[0]]

def load_data():
	data = {}
	connection = pymysql.connect(
							 host='localhost',
                             user='root',
                             password='',
                             db='alexa_md',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM symptoms")
		fetched = cursor.fetchall()

		for fetch in fetched:
			data[fetch['symptom']] = fetch['id']

	connection.close()

	return data

def get_symptom_ids(symptoms):
	symptom_ids = []
	data = load_data()

	for symptom in symptoms:
		if symptom in data.keys():
			symptom_ids.append(data[symptom])
		else:
			symptom_ids.append(decode(symptom.lower(), data))	

	return symptom_ids