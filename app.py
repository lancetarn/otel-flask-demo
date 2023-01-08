import os
from random import randint
from time import sleep

from flask import Flask
import requests

app = Flask(__name__)

SERVICE_NAME = os.getenv("SERVICE_NAME")
OTHER_NAME = os.getenv("OTHER_NAME")
OTHER = f"http://{OTHER_NAME}:8000"


@app.route("/")
def ping():
    sleep(0.005)
    url = OTHER
    if randint(0, 9) == 5:
        url = f"{url}/whiff"
    else:
        url = f"{OTHER}/pong"

    res = requests.get(url)
    return res.text


@app.route("/pong")
def pong():
    sleep(0.005)
    return "pong"


@app.route("/whiff")
def whiff():
    raise RuntimeError("Whiff!")
