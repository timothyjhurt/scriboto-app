#https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972
from flask import Flask, render_template
from flask import g
import multithreading as multi
import showResults as results
import Scriboto_Record as SR
import Scriboto_Upload as SU
import os
import time


try:
    file_name_base = str(time.time()).split('.')[0]+str(time.time()).split('.')[1]+str(os.environ['USERPROFILE'])[-3:]
except:
    file_name_base = str(time.time()).split('.')[0]+str(time.time()).split('.')[1]+str(os.environ['HOME'])[-3:]
f = open('file_name.txt','w')
f.write(file_name_base)
f.close()

app = Flask(__name__)
@app.route("/")


def main():
    return render_template('indexStart.html')

@app.route('/showResults')
def showResults():
	results.showResults(file_name_base[:15]+".csv")
	return render_template('results.html')

@app.route('/showHome')
def showHome():
	#print("HERE!!")
	return render_template('indexStart2.html')

@app.route('/startRecording')
def startRecording():
	multi.Start()
	return render_template('indexStop.html')


@app.route('/startRecording2')
def startRecording2():
	multi.Start2()
	return render_template('indexStop.html')


@app.route('/stopRecording')
def stopRecording():
	multi.Stop()
	SR.record_chunk(RECORD_SECONDS = 1, WAVE_OUTPUT_FILENAME = file_name_base[:15]+"_x.wav")
	SU.upload_blob("forbetatesting", file_name_base[:15]+"_x.wav", file_name_base[:15]+"_x.wav")
	a=0
	while a==0:
		try:
			results.showResults(file_name_base[:15]+".csv")
			a=1
		except:
			time.sleep(5)
	return render_template('results.html')


if __name__ == "__main__":
    app.run()
