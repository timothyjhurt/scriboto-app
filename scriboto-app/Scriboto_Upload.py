import datetime
import os
from os import listdir
from os.path import isfile, join
from google.cloud import storage
import time
import config

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./api/apikey.json"

bucket = "forbetatesting"
mypath = "./"
ignore_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
file_to_upload = 10
print(file_to_upload)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
	"""Uploads a file to the bucket."""
	storage_client = storage.Client()
	bucket = storage_client.get_bucket(bucket_name)
	blob = bucket.blob(destination_blob_name)
	blob.upload_from_filename(source_file_name)

def upload_files():
	print("YOU ARE HERE..........")
	global file_to_upload
	#print("current file number", str(file_to_upload))
	file_name_file = open('./file_name.txt', 'r')
	file_name = file_name_file.read()
	all_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	#print("TRYING UPLOAD")
	for current_file in all_files:
		if not(current_file in ignore_files):
			print("Current file", str(current_file), "compared to", file_name + str(file_to_upload) + '.wav')
			if str(current_file) == file_name + str(file_to_upload) + '.wav':
				upload_blob(bucket, current_file, current_file)
				print("*** finished uploading file", current_file)
				ignore_files.append(current_file)
				file_to_upload = file_to_upload + 1
			elif str(current_file) == file_name + "_x.wav":
				upload_blob(bucket, current_file, current_file)
				file_to_upload = 10
				print("*** finished uploading file", file_to_upload)

def scriboto_upload_files():
	config.upload_const=0
	print("STARTED UPLOAD")
	while True:
		if config.upload_const==0:
			upload_files()
			time.sleep(15)
		else:
			print('upload stopped')
			return
