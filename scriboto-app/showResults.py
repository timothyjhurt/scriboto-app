import shutil
from google.cloud import storage
import pandas as pd
import time
from string import punctuation

bucket = "output4ui"
med_df = pd.read_csv("drugs_84566.csv")
# Read in body parts
body_df = pd.read_csv("body_part_66144_union.csv")

def download_blob(bucket_name, source_blob_name, destination_file_name):
	"""Downloads a blob from the bucket."""
	storage_client = storage.Client()
	bucket = storage_client.get_bucket(bucket_name)
	blob = bucket.blob(source_blob_name)

	blob.download_to_filename(destination_file_name)

	print('Blob {} downloaded to {}.'.format(
		source_blob_name,
		destination_file_name))

def Convert_To_Doctor_Speak(convo_df):

	convo_df = convo_df["sentence"]
	print("-----Converting to Doctor Speak-----", convo_df.shape, convo_df.head())

	# Read in clinical findings
	clinical_df = pd.read_csv("finding.csv")
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
	# Read in medications
	# med_df = pd.read_csv("drugs_84566.csv")
	# # Read in body parts
	# body_df = pd.read_csv("body_part_66144_union.csv")

	timing = ['seconds', 'sec', 'second', 'minute', 'min', 'minutes', 'hour',\
	'hours', 'hr', 'wk', 'week', 'weeks', 'mo', 'month', 'months', 'yr', 'year',\
	 'years','1','2','3','4','5','6','7','8','9','0','one','two','three','four',\
	 'five','six','seven','eight','nine','ten']

	Doctor_Speak_Results = []
	for i in range(convo_df.shape[0]):

		EHR_sent = []

		for word in convo_df[i].split():
			# clean up strings
			word = word.strip(punctuation)
			word = word.replace("_", " ")
			# prep word for regex expressions
			word_bracket = ''
			for letter in word:
				word_bracket = word_bracket + '[' + letter + ']'
				# pass over stop words
			if word.lower() in stop_words:
				pass
			# extract timing words
			elif word in timing:
				EHR_sent.append(word)
			# make sure the word is longer than 4 letters
			elif len(word)<5:
				pass
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
			else:
				pass
			if "I'm" in EHR_sent:
					EHR_sent.remove("I'm")
		Doctor_Speak_Results.append(" ".join(EHR_sent))
	df_final = pd.DataFrame(Doctor_Speak_Results)
	print("successfully converted to doctor speak", df_final.head())
	return df_final

def generateResultsDrSpeak():
	#read in conversation
	print("----- Generating DR SPEAK HTML -----")
	pd_conversation_input = pd.read_csv("labeled_output.csv")
	pd_conversation = Convert_To_Doctor_Speak(pd_conversation_input)
	pd_conversation["predicted_label"] = pd_conversation_input["predicted_label"]

	print("Results", pd_conversation.head())

	sections = pd_conversation["predicted_label"].unique()

	pd_conversation_section_list = {}

	print("Transcript Section", sections)
	for section in sections:
		print("Here 1a", section)
		new_pd = pd_conversation[pd_conversation["predicted_label"] == section]
		print("Here 1b", new_pd.columns.values, new_pd.head(), "here", new_pd[0])
		pd_conversation_section_list[section] = new_pd[0][new_pd[0]!=""].str.cat(sep=' <br> ')
		print("********Here 1c********", section, pd_conversation_section_list[section]=="")

	final_sections = []
	full_names=['History of Present Illness (HPI)', 'Past Medical History (PMH)',"Allergies", 'Medication',"Family History",\
	"Social History","Physical Examination (PE)","Instructions","Miscellaneous"]
	sections=["HPI", "PMH", "allergies", "medication", "family history", "social history", "PE", "instructions", "MISC"]
	combined=[]
	for i in range(len(full_names)):
		combined.append((sections[i], full_names[i]))

	for section in combined:
		if section[0] in pd_conversation_section_list:
			final_sections.append(section)

	return final_sections, pd_conversation_section_list

def showResults(filename):
	filedownloaded = False
	while not(filedownloaded):
		try:
			download_blob(bucket, filename, "labeled_output.csv")
			filedownloaded = True
		except:
			time.sleep(5)
			print("waiting for output ui file")

	pd_conversation = pd.read_csv("labeled_output.csv")

	sections = pd_conversation["predicted_label"].unique()

	pd_conversation_section_list = {}

	for section in sections:
		new_pd = pd_conversation[pd_conversation["predicted_label"] == section]
		pd_conversation_section_list[section] = new_pd["sentence"].str.cat(sep=' <br> ')

	final_sections = []
	full_names=['History of Present Illness (HPI)', 'Past Medical History (PMH)',"Allergies", 'Medication',"Family History",\
	"Social History","Physical Examination (PE)","Instructions","Miscellaneous"]
	sections=["HPI", "PMH", "allergies", "medication", "family history", "social history", "PE", "instructions", "MISC"]
	combined=[]
	for i in range(len(full_names)):
		combined.append((sections[i], full_names[i]))

	for section in combined:
		if section[0] in pd_conversation_section_list:
			final_sections.append(section)


	file_first = open('./results_top.html', 'r')
	first_section = file_first.read()
	file_first.close()
	file_middle = open('./results_middle.html', 'r')
	middle_section = file_middle.read()
	file_middle.close()
	file_bottom = open('./results_bottom.html', 'r')
	bottom_section = file_bottom.read()
	file_bottom.close()

	file = open('./templates/results.html','w')
	file.write(first_section)

	# for key in final_sections:
	# 	file.write("<h5>" + key + "</h5>")
	# 	file.write("<p class=\"w3-text-grey\">" + pd_conversation_section_list[key] + "</p>")
	# 	print("key", key)
	# 	print(pd_conversation_section_list[key])
	# file.write(middle_section)

	for key in final_sections:
		file.write("<h5>" + key[1] + "</h5>")
		file.write("<p class=\"w3-text-grey\">" + pd_conversation_section_list[key[0]] + "</p>")
		print("key", key[1])
		print(pd_conversation_section_list[key[0]])
	file.write(middle_section)

	final_sections_dr_speak, pd_conversation_section_list_dr_speak = generateResultsDrSpeak()

	for key in final_sections_dr_speak:
		if pd_conversation_section_list_dr_speak[key[0]] != "":
			file.write("<h5>" + key[1] + "</h5>")
			file.write("<p class=\"w3-text-grey\">" + pd_conversation_section_list_dr_speak[key[0]] + "</p>")
			print("key", key[1])
			print(pd_conversation_section_list_dr_speak[key[0]])

	file.write(bottom_section)
	file.close()
