import os
from random import randint
from time import sleep

import requests
from flask import Flask, Response, request, g
from opentelemetry import trace

app = Flask(__name__)

OTHER_NAME = os.getenv("OTHER_NAME")
OTHER = f"http://{OTHER_NAME}:8000"


@app.before_request
def start_custom_wrapper_span():
    tracer = trace.get_tracer(__name__)
    span = tracer.start_span("pong_business")
    trace.set_span_in_context(span)
    span.set_attribute("pong.foo", request.args.get("foo", ""))
    g.pong_business = span


@app.after_request
def close_wrapper_span(response: Response):
    g.pong_business.end()
    return response


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
    sleep(0.005)
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("ponging") as current:
        current.set_attribute("pong.ponging", randint(0, 5))

    return "pong"


@app.route("/whiff")
def whiff():
    raise RuntimeError("Whiff!")
