import datetime
import os
from os import listdir
from os.path import isfile, join
from google.cloud import storage
import time

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./api/apikey.json"

bucket = "forbetatesting"
mypath = "./"
ignore_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]


def upload_blob(bucket_name, source_file_name, destination_blob_name):
	"""Uploads a file to the bucket."""
	storage_client = storage.Client()
	bucket = storage_client.get_bucket(bucket_name)
	blob = bucket.blob(destination_blob_name)

	blob.upload_from_filename(source_file_name)


def upload_files():
	all_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	for current_file in all_files:
		if not(current_file in ignore_files):
			if current_file[-3:]=='wav':
				upload_blob(bucket, current_file, current_file)
				ignore_files.append(current_file)

def scriboto_upload_files():
	print("STARTED UPLOAD")
	while True:
		upload_files()
		time.sleep(5)
