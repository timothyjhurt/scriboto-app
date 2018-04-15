import pyaudio
import wave
import datetime
import time
import math
import os
import config

try:
	from importlib import reload
except:
	pass
#length of chunk in seconds
chunk_length = 5

def record_chunk(RECORD_SECONDS = 5, WAVE_OUTPUT_FILENAME = "file.wav"):
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 16000
	CHUNK = 1024
	a=0
	while a==0:
		audio = pyaudio.PyAudio()
		info = audio.get_host_api_info_by_index(0)
		numdevices = info.get('deviceCount')
		if str(numdevices)[0]!='0':
			a=1
		else:
			reload(pyaudio)
	# for i in range(0, numdevices):
	#     if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
	#         print "Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name')
	# start Recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,
					rate=RATE, input=True,
					frames_per_buffer=CHUNK)
	#print("recording         ", datetime.datetime.now())
	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
	#print("finished recording", datetime.datetime.now())
	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()

	waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()

def record_conversation(convo_length = 60*15):
	#print("STARTED RECORDING")
	config.record_const=0
	number_of_files = math.ceil(convo_length/chunk_length)
	f=open('file_name.txt','r')
	file_name_base=f.read()
	f.close()
	list_of_filenames = [file_name_base + str(index+10) + ".wav" for index in range(int(number_of_files))]
	#print(list_of_filenames)
	for filename in list_of_filenames:
		if config.record_const==0:
			record_chunk(RECORD_SECONDS = chunk_length, WAVE_OUTPUT_FILENAME = filename)
		else:
			print('record stopped')
			return
#record_conversation(convo_length =  300)

print("SR_Loaded_and_Done")
