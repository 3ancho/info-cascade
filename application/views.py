from application import app
from flask import render_template, request, flash, redirect, url_for, session 
from google.appengine.ext import db
from models import *
from forms import *
import time, random


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game/create', methods=["GET", "POST"])
def create_game():
    form = GameForm()
    if form.validate_on_submit():
        timestamp = time.strftime('-%Y%m%d.%H%M%S')
        
        if random.randint(1,2) == 1:
            one = "b"
            two = "gg"
        else:
            one = "g"
            two = "bb"
        init = "%s%s".format(two,one)
        game = Game(title=form.title.data + timestamp, 
                    max_turns=form.max_turns.data,
                    contains=init,
                    current_turn=1)
        key = game.put()
        flash("Game created!", "success") 
        
        uri = '/playgame/{}'.format(key)
        if init == "bgg":
            contains = "Two Green one Black"
        else:
            contains = "Two Black one Green"
        return render_template('create.html', form=form, uri=uri, contains=contains) 
    return render_template('create.html', form=form)

@app.route('/games')
def show_games():
    games = db.GqlQuery("SELECT * "
                        "FROM Game "
                        "ORDER BY created")
    return render_template('show_games.html', games=games)

@app.route('/playgame/<key>', methods=["GET", "POST"])
def play_game(key):
    '''
    When GET, show use the previous guesses. A modal will display the drawn result.
    Then the player will be provide a form asking for name and
    '''
    game = db.get(str(key)) 
    rule = "There are three marbles, 2 black 1 green or 1 back 2 green"
  

    # Get plays belongs to the game
    plays = db.GqlQuery("SELECT * "
                        "FROM Play "
                        "WHERE game = :1 "
                        "ORDER BY played", game)
    black = 0
    green = 0
    for play in plays:
        if play.guess == "g": 
            black += 1 
        else:
            green += 1 

    index = random.randint(0,2)
    drawn = game.contains[index]
    # Handle POST
    # form = PlayForm()
    # if form.validate_on_submit():
    if request.method == "POST":

        play = Play(player=request.form['player'], guess=request.form['guess'], drawn=session['drawn'], game=game)
        # Modify >> play.game.current_turn += 1
        game.current_turn += 1
        game.put()
        # Select * from play where parent = <key> 
        play_key = play.put()
        
        session.pop('drawn')
        # resirect to home
        return render_template('play_game.html', key=key, game=game, black=black, green=green)
    # Handle GET
    flash("Welcome!")
    session['drawn'] = drawn 
    return render_template('play_game.html', key=key, game=game, drawn=drawn, rule=rule, black=black, green=green)
    
