from application import app
from models import *
from forms import *
from flask import render_template, request, flash, redirect, url_for

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game/create', methods=["GET", "POST"])
def create_game():
    form = GameForm()
    if form.validate_on_submit():
        game = Game(title=form.title.data, 
                    max_turns=form.max_turns.data)
        game.put()
        flash("Game created!", "success") 
        return redirect(url_for('create_game')) 
    return render_template('create.html', form=form)

@app.route('/games')
def list_games():
    pass
