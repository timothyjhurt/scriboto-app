#NEW
#https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972
from flask import Flask, render_template
from flask import g
import multithreading as multi
import showResults as results
import Scriboto_Record as SR
import Scriboto_Upload as SU
import os
import time
import doctor_Speak as DoctorSpeak
try:
	from importlib import reload
except:
	pass

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def main():
	return render_template('indexStart.html')

@app.route('/showResults')
def showResults():
	f=open('file_name.txt','r')
	file_name_base=f.read()
	f.close()
	results.showResults(file_name_base+".csv")
	return render_template('results.html')

@app.route('/showHome')
def showHome():
	reload(multi)
	reload(SR)
	return render_template('indexStart.html')

@app.route('/startRecording')
def startRecording():
	try:
		file_name_base = str(time.time()).split('.')[0]+str(time.time()).split('.')[1]+str(os.environ['USERPROFILE']).split("\\")[-1]
	except:
		file_name_base = str(time.time()).split('.')[0]+str(time.time()).split('.')[1]+str(os.environ['HOME']).split("/")[-1]
	f = open('file_name.txt','w')
	f.write(file_name_base)
	f.close()
	multi.Start()
	return render_template('indexStop.html')


@app.route('/stopRecording')
def stopRecording():
	multi.Stop()
	f=open('file_name.txt','r')
	file_name_base=f.read()
	f.close()
	SR.record_chunk(RECORD_SECONDS = 1, WAVE_OUTPUT_FILENAME = file_name_base+"_x.wav")
	SU.upload_blob("forbetatesting", file_name_base+"_x.wav", file_name_base+"_x.wav")
	a=0
	while a==0:
		try:
			results.showResults(file_name_base+".csv")
			a=1
		except:
			time.sleep(5)
	multi.terminate_remaining()
	return render_template('results.html')

@app.route('/drSpeak')
def drSpeak():
	print("Starting Doctor Speak")
	DoctorSpeak.showResultsDrSpeak()
	print("Finished creating Doctor Speak File")
	return render_template('results_drSpeak.html')

if __name__ == "__main__":
	app.run()
