#!/usr/bin/env python
"""
Fetches data from the Open Data Archive.
"""

from astropy.time import Time
import requests
import sys

# API = "http://35.236.84.6:5001/api"
API = "http://seti.berkeley.edu/opendata/api"

now = Time.now().mjd
params = {"target": "", "time-start": now - 365}
json = requests.get(f"{API}/query-files", params=params).json()
if json["result"] != "success":
    print(json, file=sys.stderr)
    raise IOError("API failure")
data = json["data"]

# Sort by most recent first
data.sort(key=lambda x: -x["mjd"])
print(f"fetched {len(data)} entries. most recent:")
for entry in data[:10]:
    print(entry)
