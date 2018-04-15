#!/usr/bin/python

#import _thread as thread
import time
import Scriboto_Record as SR
import Scriboto_Upload as SU
import multiprocessing as mp
import random
import string



def Start():
# Setup a list of processes that we want to run
	global processes
	processes = []
	processes.append(mp.Process(target=SU.scriboto_upload_files, args=(), name='Upload'))
	processes.append(mp.Process(target=SR.record_conversation, args=(), name='Recording'))
	# Run processes
	for p in processes:
		p.daemon = True
		p.start()


def Stop():
	time.sleep(5) #SR.chunk_length
	for p in range(len(processes)):
		if p == 1:
			processes[p].terminate()

def terminate_remaining():
	for p in range(len(processes)):
		if p==0:
			processes[p].terminate()
	time.sleep(.3)


print("MThreading Loaded And Done")
