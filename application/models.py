from google.appengine.ext import db
import datetime

class Game(db.Model):
    title = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    users = db.StringListProperty()
    times = db.ListProperty(datetime.datetime)
    resp_times = db.ListProperty(datetime.datetime)
    max_turns = db.IntegerProperty()
    current_turn = db.IntegerProperty()
