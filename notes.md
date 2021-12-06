# python3 -m venv env
to start virutal environment

# source env/bin/activate

# pip3 install flask

# pip3 freeze > requirements.txt
send all that is installed to requirements.txt

# this is if you clone a file and you have to download the files on your pc
# python3 -m pip3 install -r requirements.txt
to install packages from the requirements file and tell pip to install all of the packages in this file 


START
# touch app.py

IN APP.PY
# from flask import Flask

# DEBUG=True

# PORT=8000

# app = Flask(__name__)

# if __name__ == '__main__':
#   app.run(debug=DEBUG,port=PORT)



PSYCOPG2-BINARY
- lets our application connect to the database

PEEWEE 
- ORM - (object relational mapping) - allows us to create models and allows us to query to DB in Flask app

