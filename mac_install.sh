curl -O "https://repo.continuum.io/archive/Anaconda2-5.1.0-MacOSX-x86_64.sh"
bash ./Anaconda2-5.1.0-MacOSX-x86_64.sh

conda update setuptools
pip install -e .
cd scriboto-app
export FLASK_APP=app.py
python -m flask run
