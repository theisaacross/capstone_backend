#this file is analogous to statController.js
import models
# a blueprint is a way to create a self-contained grouping of related functionalities in an app
# we are going to use a blueprint as a controller

from flask import Blueprint

#first argument is blueprint's name
#second argument is the import_name
stats = Blueprint('stats', 'stats')

@stats.route('/')
def index():
    return "index route is working"