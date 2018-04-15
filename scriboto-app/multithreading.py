#!/usr/bin/python

#import _thread as thread
import time
import Scriboto_Record as SR
import Scriboto_Upload as SU
# import multiprocessing as mp
import threading
import random
import string
import config

def Start():
# Setup a list of processes that we want to run
	upload_thread = threading.Thread(target=SU.scriboto_upload_files)
	record_thread = threading.Thread(target=SR.record_conversation)
	# Run processes
	upload_thread.start()
	record_thread.start()

def Stop():
	time.sleep(6) #SR.chunk_length
	config.record_const=1

def terminate_remaining():
	config.upload_const=1
	time.sleep(.3)

print("MThreading Loaded And Done")
