from peewee import *

#flask_login to set up our user model, sessions, logins and authentication
from flask_login import UserMixin

DATABASE = SqliteDatabase('stats.sqlite') # creates stats database

# defining our model

class Score(Model):
    # add in userId or username
    date = DateField()
    location = CharField()
    hole = IntegerField()
    score = IntegerField()
    putts = IntegerField()
    
    class Meta: #connects us to the db
        database = DATABASE

# our user class inherits certain methods and properites from UserMixin
class User(UserMixin, Model):
    username= CharField(unique=True)
    password = CharField()

    class Meta: #connects us to the db
        database = DATABASE


#define a method that will get called when app is started
def initialize():
    DATABASE.connect()

    # we need to create the tables based on our schemas
    DATABASE.create_tables([User, Score], safe=True)
    print('Connected to the DB and created tables')
    DATABASE.close()

