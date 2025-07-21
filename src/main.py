import flask
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    try:
        with open("lifeGoals.txt", "r") as f:
            goals = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        goals = []
    return render_template("index.html", goals=goals)

if __name__ == "__main__":
    app.run(debug=True)
