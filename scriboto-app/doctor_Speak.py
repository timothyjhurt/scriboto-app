import pandas as pd
import time
from string import punctuation

# Read in medications
med_df = pd.read_csv("drugs_84566.csv")
# Read in body parts
body_df = pd.read_csv("body_part_66144_union.csv")


def Convert_To_Doctor_Speak(convo_df):

	convo_df = convo_df["sentence"]
	# print("Converting to Doctor Speak", convo_df.shape, convo_df.head())

	# Read in clinical findings
	clinical_df = pd.read_csv("finding.csv")
	# print(clinical_df.head())
	# Read in stopwords
	stop_words = ['i', 'me', 'my', 'myself','we','our','ours','ourselves','you','you\'re','you\'ve','you\'ll',\
	'you\'d','your','yours','yourself','yourselves','he','him','his','himself','she','she\'s',\
	'her','hers','herself','it','it\'s','its','itself','they','them','their','theirs','themselves',\
	'what','which','who','whom','this','that','that\'ll','these','those','am','is','are','was','were',\
	'be','been','being','have','has','had','having','do','does','did','doing','a','an','the','and',\
	'but','if','or','because','as','until','while','of','at','by','for','with','about','against',\
	'between','into','through','during','before','after','above','below','to','from','up','down',\
	'in','out','on','off','over','under','again','further','then','once','here','there','when',\
	'where','why','how','all','any','both','each','few','more','most','other','some','such','no',\
	'nor','not','only','own','same','so','than','too','very','s','t','can','will','just','don',\
	'don\'t','should','should\'ve','now','d','ll','m','o','re','ve','y','ain','aren','aren\'t',\
	'couldn','couldn\'t','didn','didn\'t','doesn','doesn\'t','hadn','hadn\'t','hasn','hasn\'t',\
	'haven','haven\'t','isn','isn\'t','ma','mightn','mightn\'t','mustn','mustn\'t','needn',\
	'needn\'t','shan','shan\'t','shouldn','shouldn\'t','wasn','wasn\'t','weren','weren\'t',\
	'won','won\'t','wouldn','wouldn\'t']
	# # Read in medications
	# med_df = pd.read_csv("drugs_84566.csv")
	# # Read in body parts
	# body_df = pd.read_csv("body_part_66144_union.csv")

	timing = ['seconds', 'sec', 'second', 'minute', 'min', 'minutes', 'hour', 'hours', 'hr', 'wk', 'week', 'weeks', 'mo', 'month', 'months', 'yr', 'year', 'years']

	Doctor_Speak_Results = []
	for i in range(convo_df.shape[0]):

		EHR_sent = []
		# print("SENTENCE: ", convo_df[i])

		for word in convo_df[i].split():
			print("HEREEEEE", word)
			# clean up strings
			word = word.strip(punctuation)
			word = word.replace("_", " ")
			# prep word for regex expressions
			word_bracket = ''
			for letter in word:
				word_bracket = word_bracket + '[' + letter + ']'
				# pass over stop words
			if word.lower() in stop_words:
				print(word)
				word=' '
			# extract timing words
			elif word in timing:
				EHR_sent.append(word)
			# extract clinical entities
			elif (clinical_df['term'].str.contains(r'\b' + word_bracket + r'\b')).any() == True:
				EHR_sent.append(word)
			# extract body parts
			elif (body_df['term'].str.contains(r'\b' + word_bracket + r'\b')).any() == True:
				EHR_sent.append(word)
			# extract medications
			elif (med_df['term'].str.contains(r'\b' + word_bracket + r'\b')).any() == True:
				EHR_sent.append(word)
			# take out unecessary words
			if "I'm" in EHR_sent:
				EHR_sent.remove("I'm")
		# print("appending this:", EHR_sent)
		Doctor_Speak_Results.append(" ".join(EHR_sent))
	df_final = pd.DataFrame(Doctor_Speak_Results)
	# print("successfully converted", df_final.head())
	return df_final


def showResultsDrSpeak():
	print("Starting show results")
	#read in conversation
	print("Loading labeled output")
	pd_conversation_input = pd.read_csv("labeled_output.csv")
	pd_conversation = Convert_To_Doctor_Speak(pd_conversation_input)
	# print("Finished Converting labeled output")
	pd_conversation["predicted_label"] = pd_conversation_input["predicted_label"]

	print(pd_conversation.head())

	sections = pd_conversation["predicted_label"].unique()

	pd_conversation_section_list = {}

	print("Here1c", sections)
	for section in sections:
		print("Here 1a", section)
		new_pd = pd_conversation[pd_conversation["predicted_label"] == section]
		print("Here 1b", new_pd.columns.values, new_pd.head(), "here", new_pd[0])
		pd_conversation_section_list[section] = new_pd[0].str.cat(sep=' <br> ')
		print(pd_conversation_section_list[section])

	print("fixed")
	file_last = open('results_bottom.html','r')
	last_section = file_last.read()
	file_last.close()

	final_sections = []

	print("Here1")
	for section in ["HPI", "PMH", "allergies", "medication", "family history", "social history", "PE", "instructions", "MISC"]:
		if section in pd_conversation_section_list:
			final_sections.append(section)

	file_first = open('./results_top_drspeak.html', 'r')
	first_section = file_first.read()
	file_first.close()

	print("Here2")
	file = open('./templates/results_drSpeak.html','w')
	file.write(first_section)
	for key in final_sections:
		file.write("<h4>" + key + "</h4>")
		file.write("<p>" + pd_conversation_section_list[key] + "</p>")
		print("key", key)
		print(pd_conversation_section_list[key])
	file.write(last_section)
	file.close()
	print("Finished Doctor Speak")



print("Doctor Speak Loaded1")
