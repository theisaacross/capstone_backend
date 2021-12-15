#this file is analogous to statController.js
import models
# a blueprint is a way to create a self-contained grouping of related functionalities in an app
# we are going to use a blueprint as a controller

from flask import Blueprint, request, jsonify #request is basically req.body

from flask_login import login_required , current_user

# useful tools from peewee
from playhouse.shortcuts import model_to_dict

#first argument is blueprint's name
#second argument is the import_name
stats = Blueprint('stats', 'stats')

#index
@stats.route('/', methods=['GET'])
# @login_required
def index():
    result = models.Score.select()
    print(result) #looks like SQL

    #use a loop to populate all models to dictionaries
    # score_dicts = [model_to_dict(score) for score in result]
    current_user_score_dicts = [model_to_dict(score) for score in current_user.stats]


    for score_dict in current_user_score_dicts:
        score_dict['user'].pop('password')
        
    return jsonify(
        data=current_user_score_dicts,
        message=f"Successfully found {len(current_user_score_dicts)} scores",
        status=200
    ),200

#create route
@stats.route('/', methods=['POST'])
@login_required
def create_score():
    # .get_json() attached to the request will extract JSON from the request body. (like req.body)
    payload = request.get_json()
    print(payload) #shows the request

    new_score = models.Score.create(user=current_user.id, date=payload['date'], location=payload['location'], hole=payload['hole'], score=payload['score'], putts=payload['putts'])
    #^ this creates a new model with our schema

    score_dict = model_to_dict(new_score)
    #^ converts model to dictionary

    score_dict['user'].pop('password')

    return jsonify(
        data=score_dict,
        message='Successfully created score',
        status=201
    ), 201

#show route
@stats.route('/<id>', methods=['GET'])
@login_required
def get_score(id):
    score = models.Score.get_by_id(id)
    print(score)
    current_score= model_to_dict(score)
    current_score['user'].pop('password')

    return jsonify(
        data= current_score,
        message="Success",
        status=200
    ), 200

#update route
@stats.route('/<id>', methods=['PUT'])
@login_required
def update_score(id):
    payload = request.get_json() #grabs request
    
    update_query = models.Score.update(date=payload['date'], location=payload['location'], hole=payload['hole'], score=payload['score'], putts=payload['putts']).where(models.Score.id == id).execute()

    print(payload)
    return jsonify(
        data= model_to_dict(models.Score.get_by_id(id)),
        message= "Updated Successfully",
        status= 200
    ), 200

#delete route
@stats.route('/<id>', methods=['DELETE'])
@login_required
def delete_score(id):
    delete_query = models.Score.delete().where(models.Score.id == id)
    rows_deleted = delete_query.execute()
    print(rows_deleted)
    #if no rows were deleted return 0

    return jsonify(
        data={},
        message="Successfully deleted score",
        status=200
    ),200

