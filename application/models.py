from google.appengine.ext import db
import datetime

class Game(db.Model):
    title = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    max_turns = db.IntegerProperty()
    current_turn = db.IntegerProperty()
    contains = db.StringProperty(required = True)
    
class Play(db.Model):
    player = db.StringProperty(required = True)
    played = db.DateTimeProperty(auto_now_add = True)
    turn = db.IntegerProperty()
    game = db.ReferenceProperty(Game)

