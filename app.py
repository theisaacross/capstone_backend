from flask import Flask, jsonify

#
from resources.stats import stats

#this statement will import all variables and methods/functions from a file as properties on the model object
import models

#import our package for handling cors
from flask_cors import CORS
#^^ our origin is 8000 and react's origin is 3000 so we need to whitelist 3000 so our frontend can make requests

DEBUG=True

PORT=8000

app = Flask(__name__) #like const app = express()

#whitelisting
CORS(stats, origin=['http://localhost:3000'], supports_credentials=True) #support allows cookies and sessions for auth

#use this blueprint( component/controller of the app) to handle anything related to stats
app.register_blueprint(stats, url_prefix='/api/v1/stats')

# routes
@app.route('/test')
def test():
    return jsonify(['hello', 'hi'])



if __name__ == '__main__': # like app.listen
    #when the app starts, set up DB/tables
    models.initialize()
    #run initialize before app.run
    app.run(debug=DEBUG,port=PORT)