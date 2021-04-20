#!/usr/bin/env python
"""
Fetches data from the Open Data Archive.
"""

from astropy.time import Time
import os
import requests
import sys
from urllib.request import urlretrieve

NUM_FILES = 2
DATA_DIR = "/d/astrodata"
if not os.path.exists(DATA_DIR):
    print(f"please mount {DATA_DIR}")
    sys.exit(1)

# API = "http://35.236.84.6:5001/api"
API = "http://seti.berkeley.edu/opendata/api"
GIGABYTE = 1024 ** 3

# Find HDF5 files from the last year
now = Time.now().mjd
params = {"target": "", "file-types": "HDF5", "time-start": now - 365}
json = requests.get(f"{API}/query-files", params=params).json()
if json["result"] != "success":
    print(json, file=sys.stderr)
    raise IOError("API failure")

# At most 5 gig in size
data = [x for x in json["data"] if x["size"] <= 5 * GIGABYTE]

# Drop the 0001.h5, those are high-time-resolution / low-frequency-resolution
data = [x for x in data if not x["url"].endswith("0001.h5")]

# Sort by most recent first
data.sort(key=lambda x: -x["mjd"])
data = data[:NUM_FILES]

# Download things
for entry in data:
    url = entry["url"]
    fname = url.split("/")[-1]
    dest = os.path.join(DATA_DIR, fname)
    print(entry)
    if os.path.exists(dest):
        print(dest, "exists")
    else:
        print("downloading", dest)
        urlretrieve(url, dest)
