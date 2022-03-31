from flask import Flask, render_template, request, session
import json
import os
from datetime import timedelta, datetime
from random import randint


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "!yw2gC8!BeM3"

# Páginas


@app.before_first_request
def set_date():
    session.permanent = True
    session["lifes"] = 3
    app.permanent_session_lifetime = timedelta(days=365)


@app.route("/set")
def change_date():
    f = open(os.path.join(app.static_folder, "data.json"), "r+")
    data = json.load(f)
    f.close()
    data[0]["game_id"] = randint(0, 13)
    data[0]["tomorrow"] = datetime.today().strftime('%Y-%m-%d')
    f = open(os.path.join(app.static_folder, "data.json"), "w+")
    f.write(json.dumps(data))


@app.route("/", methods=['GET', 'POST'])
def homepage():
    f = open(os.path.join(app.static_folder, "data.json"), "r+")
    data = json.load(f)
    game_id = int(data[0]["game_id"])
    if request.method == 'POST':
        if request.form['guess'] == "teste":
            tomorrow = datetime.today() + timedelta(days=1)
            tomorrow = tomorrow.strftime('%Y-%m-%d')
            data[game_id]["viewed"] = True
            data[0]["game_id"] = str(randint(0, 13))
            data[0]["tomorrow"] = tomorrow
            f = open(os.path.join(app.static_folder, "data.json"), "w+")
            f.write(json.dumps(data))
            f.close()
    if datetime.today().strftime('%Y-%m-%d') == data[0]["tomorrow"]:
        change_date()
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
                           game_name=game_name, game_image=game_image)


if __name__ == "__main__":
    app.run(debug=True)
