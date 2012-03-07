from application import app
from flask import render_template, request, flash, redirect, url_for
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
        init = "{}{}".format(two,one)
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
    form = PlayForm()
    game = db.get(str(key)) 
    rule = "There are three marbles, 2 black 1 green or 1 back 2 green"
  

    # Get plays belongs to the game
    plays = db.GqlQuery("SELECT * "
                        "FROM Play "
                        "WHERE game = :1 "
                        "ORDER BY played", key)
    black = 0
    green = 0
    for play in plays:
        if play.result == "g": 
            black += 1 
        else:
            green += 1 


    # Handle POST
    if form.validate_on_submit():
        index = random.randint(0,2)
        drawn = game.contains[index]

        play = Play(player=form.title.data, result=drawn, game=game)
        # Modify >> play.game.current_turn += 1
        game.current_turn += 1
        game.put()
        # Select * from play where parent = <key> 
        key = play.put()
        
        flash("You got {}".format(result), "success") 
        return render_template('play_game.html', form=form, game=game, play=play)
    # Handle GET
    flash("hohoho")
    return render_template('play_game.html', form=form, key=key, plays=plays, game=game, rule=rule, black=black, green=green)
    
