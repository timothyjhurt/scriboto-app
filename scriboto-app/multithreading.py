#!/usr/bin/python

#import _thread as thread
import time
import Scriboto_Record as SR
import Scriboto_Upload as SU
import multiprocessing as mp
import random
import string

processes = []

def Start():
# Setup a list of processes that we want to run
	processes.append(mp.Process(target=SU.scriboto_upload_files, args=(), name='Upload'))
	processes.append(mp.Process(target=SR.record_conversation, args=(), name='Recording'))
	# Run processes
	for p in processes:
		p.daemon = True
		p.start()


def Start2():
# Setup a list of processes that we want to run
	processes.append(mp.Process(target=SR.record_conversation, args=(), name='Recording'))
	# Run processes
	processes[-1].daemon = True
	processes[-1].start()

def Stop():
	time.sleep(5)#SR.chunk_length)
	for p in range(len(processes)):
		if p == 1:
			processes[p].terminate()
	#terminate()
# Get process results from the output queue
#results = [output.get() for p in processes]

#Start()

print("MThreading Loaded And Done")
