from application import app
from models import *
from forms import *
from flask import render_template, request, flash, redirect, url_for
import time, random
from google.appengine.ext import db
import logging


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
                    contains=init)
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
    logging.debug("key is ", key)

    game = db.get(str(key)) 
    rule = "There are three marbles, 2 black 1 green or 1 back 2 green"
    if game.contains == "bgg":
        contains = ""
    else:
        contains = ""

    if form.validate_on_submit():
        index = random.randint(0,2)
        drawn = game.contains[index]

        play = Play(a,b,c)
        key = play.put()
        return render_template('play_game.html', form=form, game=game)
    return render_template('play_game.html', form=form, key=key, game=game, contains=contains, rule=rule)
    
