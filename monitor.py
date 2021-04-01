#!/usr/bin/env python3

import os
from flask import Flask

BASE_DIR = os.path.expanduser("~/target_logs")

app = Flask(__name__)


@app.route("/")
def index():
    return "welcome to monitor"
