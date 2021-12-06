from peewee import *

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

#define a method that will get called when app is started
def initialize():
    DATABASE.connect()

    # we need to create the tables based on our schemas
    DATABASE.create_tables([Score], safe=True)
    print('Connected to the DB and created tables')
    DATABASE.close()

