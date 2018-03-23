#pip3 install google-cloud-storage
# pip install google-cloud==0.24.0

#ensure you have Google application installed
#export GOOGLE_APPLICATION_CREDENTIALS="/Users/yannielee/Desktop/W210/W210ScribotoKey.json"
import datetime
import os
from os import listdir
from os.path import isfile, join
from google.cloud import storage
import time


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/api/apikey.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/yannielee/Desktop/W210/W210ScribotoKey.json"
bucket = "forbetatesting"
mypath = "./"
ignore_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
#print(ignore_files)
#print(os.environ)
#ignore_files = ['.DS_Store', 'pyAudio - Sandbox.ipynb', 'Scriboto - Record Process.ipynb', 'Scriboto - Upload Process.ipynb']

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    #print('File {} uploaded to {}.'.format(
    #    source_file_name,
    #    destination_blob_name))


def make_blob_public(bucket_name, blob_name):
    """Makes a blob publicly accessible."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.make_public()

    #print('Blob {} is publicly accessible at {}'.format(
    #    blob.name, blob.public_url))

def upload_files():
    all_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    #print(all_files)
    for current_file in all_files:
        if not(current_file in ignore_files):
            #print("uploading", current_file, datetime.datetime.now())
            upload_blob(bucket, current_file, current_file)
            #make_blob_public(bucket, current_file)
            #print("finished uploading", current_file, datetime.datetime.now())
            ignore_files.append(current_file)

def scriboto_upload_files():
    print("STARTED UPLOAD")
    while True:
        #print("start of loop")
        upload_files()
        time.sleep(5)
