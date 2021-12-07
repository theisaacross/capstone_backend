#this file is analogous to statController.js
import models
# a blueprint is a way to create a self-contained grouping of related functionalities in an app
# we are going to use a blueprint as a controller

from flask import Blueprint, request, jsonify #request is basically req.body

# useful tools from peewee
from playhouse.shortcuts import model_to_dict

#first argument is blueprint's name
#second argument is the import_name
stats = Blueprint('stats', 'stats')

@stats.route('/', methods=['GET'])
def index():
    result = models.Score.select()
    print(result) #looks like SQL

    #use a loop to populate all models to dictionaries
    score_dicts = []
    for score in result:
        score_dict = model_to_dict(score)
        score_dicts.append(score_dict)
        
    return jsonify(
        data=score_dicts,
        message=f"Successfully found {len(score_dicts)} scores",
        status=200
    ),200

@stats.route('/', methods=['POST'])
def create_score():
    # .get_json() attached to the request will extract JSON from the request body. (like req.body)
    payload = request.get_json()
    print(payload) #shows the request

    new_score = models.Score.create(date=payload['date'], location=payload['location'], hole=payload['hole'], score=payload['score'], putts=payload['putts'])
    #^ this creates a new model with our schema

    score_dict = model_to_dict(new_score)
    #^ converts model to dictionary

    return jsonify(
        data=score_dict,
        message='Successfully created score',
        status=201
    ), 201