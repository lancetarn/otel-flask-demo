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
    if randint(0, 9) == 5:
        raise RuntimeError("Whiff!")
    sleep(0.005)
    res = requests.get(OTHER)
    return res.text
