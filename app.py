from flask import Flask, render_template, request, session
import json
import os
from datetime import timedelta, datetime
from random import randint


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "!yw2gC8!BeM3"

# Páginas

today = datetime.today()
tomorrow = datetime.today() + timedelta(days=1)
game_id = randint(1, 10)


@app.before_first_request
def set_date():
    session.permanent = True
    session["lifes"] = 3
    app.permanent_session_lifetime = timedelta(days=31)


def change_date():
    global game_id
    global tomorrow
    tomorrow = datetime.today() + timedelta(days=1)
    game_id = randint(1, 10)


@app.route("/", methods=['GET', 'POST'])
def homepage():
    global tomorrow
    global game_id
    today = datetime.today()
    #if today.strftime('%Y-%m-%d') == tomorrow.strftime('%Y-%m-%d'):
    #    change_date()
    if session.get("lifes") is None:
        session["lifes"] = 3
    f = open(os.path.join(app.static_folder, "data.json"), "r+")
    data = json.load(f)
    game_image = data[game_id]["image"]
    game_name = data[game_id]["name"]  # Mudar diaramente automaticamente
    if request.method == 'POST':
        if request.form['guess'].casefold() != game_name.casefold():
            session["lifes"] -= 1
        else:
            session["lifes"] = -1
    return render_template("index.html", lifes=session['lifes'],
                           game_name=game_name, game_image=game_image, today=today, tomorrow=tomorrow)
    

if __name__ == "__main__":
    app.run(debug=True)

# Heroku
