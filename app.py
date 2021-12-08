from flask import Flask, jsonify

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

DEBUG=True

PORT=8000

app = Flask(__name__) #like const app = express()


#1. set up secret/key for sessions
app.secret_key = "QFG983QHIWAFK0Q1T92341NU123RQIUWHORQQWERQAKNSAOSDF"
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



#whitelisting
CORS(stats, origin=['http://localhost:3000'], supports_credentials=True) #support allows cookies and sessions for auth
CORS(users, origin=['http://localhost:3000'], supports_credentials=True)

#use this blueprint( component/controller of the app) to handle anything related to stats
app.register_blueprint(stats, url_prefix='/stats')
app.register_blueprint(users, url_prefix='/users')

# routes
@app.route('/test')
def test():
    return jsonify(['hello', 'hi'])



if __name__ == '__main__': # like app.listen
    #when the app starts, set up DB/tables
    models.initialize()
    #run initialize before app.run
    app.run(debug=DEBUG,port=PORT)