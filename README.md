# Wishful Travel App
This flask web-app is a combination of three APIs coming together to provide 
info on cities, their top 10 restaurants, and directions from Minneapolis, MN
to the city chosen by the user. Application also allows for the user to bookmark 
favorite locations. The application is run in development mode and does require
the use of libraries documented in requirements.txt.

---

# Setup

## create and activate env using:
### For windows:
python -m venv env <br />
env\Scripts\activate

### For mac/linux:
python3 -m venv env <br />
source env/bin/activate

## Install requirements and set-up environment
1) run pip install -r requirements.txt for windows <br />or run pip3 install -r requirements.txt

## enter development environment
### Windows
1) set FLASK_APP=flask_site
2) set FLASK_ENV=development
3) flask run

### Mac/Linux:
1) export FLASK_APP=flask_site in terminal
2) export FLASK_ENV=development in terminal
3) flask run to run locally (must be running in development to run locally)
127.0.0.1:5000/home/search

## initialize the database
1) flask init-db from root

## credits/sources
Flask and CSS built with a tutorial from © Copyright 2010 Pallets.
https://flask.palletsprojects.com/en/1.1.x/tutorial/