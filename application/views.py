from application import app
from models import Game
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/games')
def list_games():
    games = Game.all()
    return render_template('list_games.html', games=games)


