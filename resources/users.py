from werkzeug.datastructures import is_immutable
from werkzeug.wrappers import response
import models

from flask import Blueprint, request, jsonify

from flask_bcrypt import generate_password_hash, check_password_hash #hashes our passwords for us 

from flask_login import login_user, current_user, logout_user #this will be used for sessions

from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')


@users.route('/', methods=['GET'])
def users_index():
    return "hit users route"

@users.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    payload["username"] = payload["username"].lower()
    print(payload)

    try:
        models.User.get(models.User.username == payload['username'])
        #this will throw an error if it doesn't exist/ user is not found
        return jsonify(
            data={},
            message="A user with that username already exists",
            status=401
        ),401

    except models.DoesNotExist:
        #the user does not exist

        #scramble the password with bcrypt
        pw_hash = generate_password_hash(payload['password'])
        
        #create user
        created_user = models.User.create(
            username=payload['username'],
            password=pw_hash
        )

        login_user(created_user) #session is created and user is logged in


        created_user_dict = model_to_dict(created_user)

        created_user_dict.pop('password')
        #respond with new user

        print(current_user.username + "you are registerd")

    return jsonify(
        data=created_user_dict,
        message="Successfully registered user",
        status=201
    ),201

@users.route('/login', methods=['POST'])
def login():
    payload=request.get_json()
    payload['username']= payload['username'].lower()

    try:
        user = models.User.get(models.User.username == payload['username'])

        user_dict = model_to_dict(user)

        password_correct = check_password_hash(user_dict['password'], payload['password'])
        # argument 1 = password to check------ argument 2 is password to verify
        if (password_correct):
            login_user(user)
            user_dict.pop('password')
            print(current_user.username + "you are logged in")

            return jsonify(
                data=user_dict,
                message=f"Successfully logged in {user_dict['username']}",
                status=200
            ), 200
        else:
            return jsonify(
                data={},
                message="Username or Password is incorrect",
                status=401
            ), 401
        

    except models.DoesNotExist:
        return jsonify(
            data={},
            message="Username or password is incorrect",
            status=401
        ),401

@users.route('/logout', methods=['GET'])
def logout():
    logout_user()

    return jsonify(
        data={},
        message="Successfully logged out",
        status=200,
    ),200


#test route to show who is logged in 
@users.route('/logged_in_user', methods=['GET'])
def get_logged_in_user():

    if not current_user.is_authenticated:
        return jsonify(
            data={},
            message="No user is currently logged in",
            status=401
        ), 401
    else:
            #we can access current_user because we called login_user and set up user_loader
        print(current_user)
        user_dict = model_to_dict(current_user)
        user_dict.pop('password')
        #you now have access to the currently logged in user
        return jsonify(
            data=user_dict,
            message=f"Currently logged in as {user_dict['username']}",
            status=200
        ), 200
