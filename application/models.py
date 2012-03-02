from google.appengine.ext import db

class Game(db.Model):
    title = db.StringProperty(required = True)
    when = db.DateTimeProperty(auto_now_add = True)
