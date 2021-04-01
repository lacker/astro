#!/usr/bin/env python3

import os
from flask import Flask

BASE_DIR = os.path.expanduser("~/target_logs")


def list_files():
    """Return a list of (filename, filesize, modification time) for the files in the base dir."""
    answer = []
    for fname in os.listdir(BASE_DIR):
        full_path = os.path.join(BASE_DIR, fname)
        if os.path.isfile(full_path):
            stat = os.stat(full_path)
            answer.append((fname, stat.st_size, stat.st_mtime))
    return answer


app = Flask(__name__)


@app.route("/")
def index():
    return f"welcome to monitor: {list_files()}"
