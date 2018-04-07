import shutil
from google.cloud import storage
import pandas as pd
import time

bucket = "output4ui"

def download_blob(bucket_name, source_blob_name, destination_file_name):
	"""Downloads a blob from the bucket."""
	storage_client = storage.Client()
	bucket = storage_client.get_bucket(bucket_name)
	blob = bucket.blob(source_blob_name)

	blob.download_to_filename(destination_file_name)

	print('Blob {} downloaded to {}.'.format(
		source_blob_name,
		destination_file_name))

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

	file_last = open('results_bottom.html','r')
	last_section = file_last.read()
	file_last.close()

	final_sections = []

	for section in ["HPI", "PMH", "allergies", "medication", "family history", "social history", "PE", "instructions", "MISC"]:
		if section in pd_conversation_section_list:
			final_sections.append(section)


	file_first = open('./results_top.html', 'r')
	first_section = file_first.read()
	file_first.close()
	file = open('./templates/results.html','w')
	file.write(first_section)
	for key in final_sections:
		file.write("<h4>" + key + "</h4>")
		file.write("<p>" + pd_conversation_section_list[key] + "</p>")
		print("key", key)
		print(pd_conversation_section_list[key])
	file.write(last_section)
	file.close()
