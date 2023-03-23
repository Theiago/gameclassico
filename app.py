from flask import Flask, render_template, request, session, redirect
import json
import os
from datetime import timedelta, datetime
from database import all_game_info

# Configuration

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "!yw2gC8!BeM3"


@app.before_first_request
def set_date():
    session.permanent = True
    session["lifes"] = 3
    session["blur"] = 15
    app.permanent_session_lifetime = timedelta(days=365)

# Change the game

@app.route("/set/526535")
def change_date():
    game_infos = None
    tomorrow = datetime.today() + timedelta(days=1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')
    f = open(os.path.join(app.static_folder, "data.json"), "r+")
    while not game_infos:
        game_infos = all_game_info()
    data = json.load(f)
    f.close()

    data = {
        "name": game_infos[0][1],
        "url": game_infos[1],
        "tomorrow": tomorrow,
    }

    print(data)

    f = open(os.path.join(app.static_folder, "data.json"), "w+")
    f.write(json.dumps(data))
    f.close()
    session["lifes"] = 3
    session["blur"] = 15
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
    game_name = data['name']
    game_image = data['url']
    f.close()

    if datetime.today().strftime('%Y-%m-%d') == data['tomorrow']:
        change_date()
        redirect('/')
    if session.get("lifes") is None:
        session["lifes"] = 3
        session["blur"] = 15

    if request.method == 'POST':
        if request.form['guess'].casefold() != game_name.casefold():
            session["lifes"] -= 1
            session["blur"] -= 5
        else:
            session["lifes"] = -1
            session["blur"] = 0
    return render_template("index.html", lifes=session['lifes'],
                           game_name=game_name, game_image=game_image, data=data,
                           hours_remaining=hours_remaining, min_remaining=min_remaining, blur=session["blur"])


if __name__ == "__main__":
    app.run(debug=True)
