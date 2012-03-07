from flaskext import wtf
from flaskext.wtf import validators

class GameForm(wtf.Form):
    title = wtf.TextField('Title', validators=[validators.Required()])
    max_turns = wtf.IntegerField('Max turns', validators=[validators.Required()])

class PlayForm(wtf.Form):
    player = wtf.TextField('Your Name', validators=[validators.Required()])
