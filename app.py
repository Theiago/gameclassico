from flask import Flask, render_template, request, session, redirect
import json
import os
from datetime import timedelta, datetime
from random import randint

# Configuration

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "!yw2gC8!BeM3"


@app.before_first_request
def set_date():
    session.permanent = True
    session["lifes"] = 3
    app.permanent_session_lifetime = timedelta(days=365)

# Change the game

@app.route("/set/526535")
def change_date():
    tomorrow = datetime.today() + timedelta(days=1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')
    f = open(os.path.join(app.static_folder, "data.json"), "r+")
    data = json.load(f)
    games_total = len(data) - 1
    f.close()
    game_id = int(data[0]["game_id"])
    data[game_id]["viewed"] = True
    while data[game_id]["viewed"] == True:
        game_id = randint(1, games_total)
        data[0]["game_id"] = game_id
    data[0]["tomorrow"] = tomorrow
    f = open(os.path.join(app.static_folder, "data.json"), "w+")
    f.write(json.dumps(data))
    f.close()
    session["lifes"] = 3
    return redirect("/")

# Mainpage

@app.route("/", methods=['GET', 'POST'])
def homepage():
    h = int(datetime.today().strftime("%H"))
    m = int(datetime.today().strftime("%M"))
    total = 1440 - 60 * h - m
    hours_remaining = str(total // 60).zfill(2)
    min_remaining = str(total % 60).zfill(2)
    f = open(os.path.join(app.static_folder, "data.json"), "r+")
    data = json.load(f)
    game_id = int(data[0]["game_id"])
    f.close()
    if datetime.today().strftime('%Y-%m-%d') == data[0]["tomorrow"]:
        change_date()
        redirect('/')
    if session.get("lifes") is None:
        session["lifes"] = 3
    game_image = data[game_id]["image"]
    game_name = data[game_id]["name"]  # Mudar diaramente automaticamente
    if request.method == 'POST':
        if request.form['guess'].casefold() != game_name.casefold():
            session["lifes"] -= 1
        else:
            session["lifes"] = -1
    return render_template("index.html", lifes=session['lifes'],
                           game_name=game_name, game_image=game_image, data=data,
                           hours_remaining=hours_remaining, min_remaining=min_remaining)


if __name__ == "__main__":
    app.run(debug=True)
