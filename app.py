from flask import Flask, jsonify, after_this_request

#
from resources.stats import stats

from resources.users import users

#this statement will import all variables and methods/functions from a file as properties on the model object
import models

#import our package for handling cors
from flask_cors import CORS
#^^ our origin is 8000 and react's origin is 3000 so we need to whitelist 3000 so our frontend can make requests

#we need to import and configure the LoginManager
from flask_login import LoginManager, login_manager

import os # this lets get app secret
from dotenv import load_dotenv
load_dotenv() #takes the environment variables from .env

DEBUG=True

PORT=8000

app = Flask(__name__) #like const app = express()


#1. set up secret/key for sessions
app.secret_key = os.environ.get("FLASK_APP_SECRET")
#2. instantiate the Login Manager 
login_manager = LoginManager()
#3. connect the app with the login_manager
login_manager.init_app(app)
#4. load current_user from the user id store in the session, shows the user object and all the score it has stored
@login_manager.user_loader
def load_user(user_id):
    try:
        user =  models.User.get_by_id(user_id)
        return user
        #it should return None, it will not raise an execption
    except models.DoesNotExist:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(
        data={'error': 'User not logged in'},
        message= "You must be logged in to use that feature.",
        status=401
    ), 401 

#whitelisting
CORS(stats, origin=['http://localhost:3000'], supports_credentials=True) #support allows cookies and sessions for auth
CORS(users, origin=['http://localhost:3000'], supports_credentials=True)

#use this blueprint( component/controller of the app) to handle anything related to stats
app.register_blueprint(stats, url_prefix='/stats')
app.register_blueprint(users, url_prefix='/users')

@app.before_request # use this decorator to cause a function to run before reqs
def before_request():

    """Connect to the db before each request"""
    print("you should see this before each request") # optional -- to illustrate that this code runs before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
    models.DATABASE.connect()

    @after_this_request # use this decorator to Executes a function after this request
    def after_request(response):
        """Close the db connetion after each request"""
        print("you should see this after each request") # optional -- to illustrate that this code runs after each request
        models.DATABASE.close()
        return response # go ahead and send response back to client
 



if os.environ.get('FLASK_ENV') != 'development':
  print('\non heroku!')
  models.initialize()

if __name__ == '__main__': # like app.listen
    #when the app starts, set up DB/tables
    models.initialize()
    #run initialize before app.run
    app.run(debug=DEBUG,port=PORT)