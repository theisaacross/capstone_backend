from flask import Flask, jsonify

#this statement will import all variables and methods/functions from a file as properties on the model object
import models

DEBUG=True

PORT=8000

app = Flask(__name__) #like const app = express()

# routes
@app.route('/test')
def test():
    return jsonify(['hello', 'hi'])



if __name__ == '__main__': # like app.listen
    #when the app starts, set up DB/tables
    models.initialize()
    #run initialize before app.run
    app.run(debug=DEBUG,port=PORT)