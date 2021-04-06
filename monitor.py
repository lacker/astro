#!/usr/bin/env python3

import os
import sys
from flask import Flask

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "data")

def list_data_files():
    """Return a list of (filename, filesize, modification time) for the files in the data dir."""
    answer = []
    for fname in os.listdir(DATA_DIR):
        full_path = os.path.join(DATA_DIR, fname)
        if os.path.isfile(full_path):
            stat = os.stat(full_path)
            answer.append((fname, stat.st_size, stat.st_mtime))
    return answer


app = Flask(__name__)

app.logger.info(f"{DATA_DIR=}")

@app.route("/")
def index():
    return f"welcome to monitor: {list_data_files()}"
