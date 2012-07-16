from google.appengine.ext import db
import datetime

class Game(db.Model):
    title = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    max_turns = db.IntegerProperty()
    current_turn = db.IntegerProperty()
    contains = db.StringProperty(required = True)
    end = db.BooleanProperty(required = True)
    password = db.StringProperty(required = True)
    
class Play(db.Model):
    player = db.StringProperty()
    turn = db.IntegerProperty()
    game = db.ReferenceProperty(Game)
    guess = db.StringProperty(required=True, choices=set([u"g", u"b"]))   # This may deleted
    drawn = db.StringProperty(required=True, choices=set([u"g", u"b"]))   # This may deleted
    played = db.DateTimeProperty(auto_now_add = True)

