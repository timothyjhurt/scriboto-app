import pyaudio
import wave
import datetime
import time
import math
import os

#length of chunk in seconds
chunk_length = 5



def record_chunk(RECORD_SECONDS = 5, WAVE_OUTPUT_FILENAME = "file.wav"):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    audio = pyaudio.PyAudio()

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


def record_conversation(convo_length = 60*5):
    #print("STARTED RECORDING")
    number_of_files = math.ceil(convo_length/chunk_length)
    f=open('file_name.txt','r')
    file_name_base=f.read()
    list_of_filenames = [file_name_base + str(index+10) + ".wav" for index in range(number_of_files)]
    #print(list_of_filenames)
    for filename in list_of_filenames:
        record_chunk(RECORD_SECONDS = chunk_length, WAVE_OUTPUT_FILENAME = filename)


#record_conversation(convo_length =  300)

print("SR_Loaded_and_Done")
