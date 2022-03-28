from flask import Flask, render_template, request, session
import json
import os
from datetime import date, timedelta
from random import randint


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "!yw2gC8!BeM3"

# Páginas


tomorrow = None


@app.before_first_request
def set_date():
    global today
    global tomorrow
    global game_id
    f = open(os.path.join(app.static_folder, "data.json"), "r+")
    data = json.load(f)
    tomorrow = date.today() + timedelta(days=1)
    today = date.today()
    game_id = randint(0, len(data))
    session.permanent = True
    session["lifes"] = 3
    app.permanent_session_lifetime = timedelta(days=31)


@app.route("/", methods=['GET', 'POST'])
def homepage():
    global today
    global tomorrow
    global game_id
    if session.get("lifes") is None:
        session["lifes"] = 3
    f = open(os.path.join(app.static_folder, "data.json"), "r+")
    data = json.load(f)
    '''if date.today() == tomorrow:
        session["lifes"] = 3
        game_id = randint(0, 7)
        tomorrow = date.today() + timedelta(days=1)'''
    game_image = data[game_id]["image"]
    game_name = data[game_id]["name"]  # Mudar diaramente automaticamente
    if request.method == 'POST':
        if request.form['guess'].casefold() != game_name.casefold():
            session["lifes"] -= 1
            return render_template("index.html",
                                   lifes=session['lifes'],
                                   game_name=game_name, game_image=game_image)
        else:
            session["lifes"] = -1
    return render_template("index.html", lifes=session['lifes'],
                           game_name=game_name, game_image=game_image)


if __name__ == "__main__":
    app.run(debug=True)

# Heroku
