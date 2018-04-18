# scriboto-app
Alpha testing the Scriboto App

### Thank you for your interest in Scriboto! Scriboto is a Data Science application being developed to save Doctors time, and improve Doctor-Patient relationships.

*Below are the instructions you should follow to install and launch Scriboto from your local computer. If you have any issues please do not hesitate to contact us at scriboto@gmail.com*

In order to ensure all of the python packages and dependencies work properly for Scriboto please download and install the most up-to-date Anaconda Distribution for Python 2.7 from https://www.anaconda.com/download/

If you already have Anaconda2, please run `conda update anaconda` before trying to install Scriboto.

Step #|Installing on a Mac|Installing on a Windows PC
---|---|---
1| Choose a directory to work out of and run: 
`git clone https://github.com/timothyjhurt/scriboto-app.git`|Choose a directory to work out of and run: 
`git clone https://github.com/timothyjhurt/scriboto-app.git`
2| Email scriboto@gmail.com to request access to a google API key for the Scriboto App | Email scriboto@gmail.com to request access to a google API key for the Scriboto App
3| Move the json key to the directory 
`scriboto-app/scriboto-app/api/`|Move the json key to the directory 
`scriboto-app\scriboto-app\api\`
4| From Terminal, navigate to 
`\scriboto-app` and run: 
`bash mac_install.sh`| Open Anaconda Prompt navigate to 
`\scriboto-app` 
and run the following commands: 
`conda update setuptools`, 
`python pip install -e .`, 
`cd scriboto-app`, 
`set FLASK_APP=app.py`
5| Once you are ready to test Scriboto, run: 
`python -m flask run` | Once you are ready to test Scriboto, run: 
`python -m flask run`
6| Open a web browser and navigate to http://127.0.0.1:5000 | Open a web browser and navigate to http://127.0.0.1:5000
7| To begin your conversation, press the "Start Recording Button"|To begin your conversation, press the "Start Recording Button"

Scriboto was designed to help categorize portions of a clinical conversation. Clinical conversation are usually rather long and usually include medical terms, descriptions of symptoms, and language related to health. If you want to test how well Scriboto performs, you should try to emulate a clinical conversation as best you can. However, it is important to remember that Scriboto is still being developed so it is wise to assume that your data could be compromised. 
  
