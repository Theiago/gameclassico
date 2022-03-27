from flask import Flask, render_template, request, make_response


app = Flask(__name__)
app.secret_key = "SEGREDOPORRA"

# Páginas


tentativas = 3


@app.route("/", methods=['GET', 'POST'])
def homepage():
    gotd = "Duke Nukem"
    resp = make_response(render_template("getcookie.html"))
    tentativas = request.cookies.get("tentativas")
    if request.method == 'POST':
        if request.form['guess'].casefold() != gotd.casefold():
            tentativas = int(tentativas)
            tentativas -= 1
            resp.set_cookie("tentativas", str(tentativas))
            return render_template("index.html",
                                   tentativas=int(tentativas), gotd=gotd)
        else:
            return render_template("index.html", tentativas=int(tentativas), gotd=gotd)
    return render_template("index.html", tentativas=int(tentativas), gotd=gotd)


@app.route("/setcookie", methods=['GET', 'POST'])
def setcookie():
    resp = make_response(render_template("setcookie.html"))
    if request.cookies.get("tentativas") is None:
        resp.set_cookie("tentativas", "3")
    if request.method == "POST":
        tentativas = int(request.cookies.get("tentativas"))
        tentativas -= 1
        resp.set_cookie("tentativas", str(tentativas))
    return resp


@app.route("/getcookie")
def getcookie():
    cookieName = request.cookies.get("tentativas")
    return "<h1>O valor do cookie é: {}</h1>".format(cookieName)


if __name__ == "__main__":
    app.run(debug=True)


'''
resp = make_response(render_template("index.html",
tentativas=tentativas, gotd=gotd))
resp.set_cookie("tentativas", tentativas)'''
