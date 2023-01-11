import os
from random import randint
from time import sleep

import requests
from flask import g, Flask
from sqlite_utils import Database


app = Flask(__name__)

OTHER_NAME = os.getenv("OTHER_NAME")
OTHER = f"http://{OTHER_NAME}:8000"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = Database(memory_name="mystuff")
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def ping():
    sleep(0.005)
    url = OTHER
    if randint(0, 9) == 5:
        url = f"{url}/whiff"
    else:
        url = f"{OTHER}/pong"

    res = requests.get(url)
    res.raise_for_status()
    return res.text


@app.route("/pong")
def pong():
    db = get_db()
    stuff = db["stuff"]
    thing = f"pony-{randint(0, 100000000)}"
    stuff.insert({"thing": thing})
    sleep(0.005)
    return "pong"


@app.route("/whiff")
def whiff():
    raise RuntimeError("Whiff!")
