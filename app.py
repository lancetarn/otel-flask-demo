import os
from flask import Flask

app = Flask(__name__)

SERVICE_NAME = os.getenv("SERVICE_NAME")
OTHER_NAME = os.getenv("OTHER_NAME")


@app.route("/")
def ping():
    return "pong"
