from flask import Flask, render_template, request, redirect, url_for
import bleach

app = Flask(__name__)

seeds = []


@app.route("/")
def index():
    return render_template("index.html", seeds=seeds)


@app.route("/add-seed", methods=["POST"])
def add_todo():
    seed = bleach.clean(request.form["seed-artist"])
    seeds.append(seed)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
