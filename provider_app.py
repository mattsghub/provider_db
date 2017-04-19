
from flask import Flask, render_template

app = Flask(__name__)

app.config["DEBUG"] = True

@app.route('/')
def hello():
    return render_template("main.html")
