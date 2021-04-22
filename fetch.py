#!/usr/bin/env python
"""
Fetches data from the Open Data Archive.
"""

from astropy.time import Time
import json
import os
import requests
import sys
from urllib.request import urlretrieve

NUM_FILES = 20
DATA_DIR = "/d/astrodata"
if not os.path.exists(DATA_DIR):
    print(f"please mount {DATA_DIR}")
    sys.exit(1)

API = "http://seti.berkeley.edu/opendata/api"
GIGABYTE = 1024 ** 3
MAX_FILE_GIGS = 5


def check_disk_space(desired):
    # Check free space
    statvfs = os.statvfs(DATA_DIR)
    free_bytes = statvfs.f_frsize * statvfs.f_bfree
    print(f"{free_bytes / GIGABYTE : .2f} GB free disk space")
    if free_bytes < desired:
        print("please free up more disk space")
        sys.exit(1)


# Find HDF5 files from the last year
now = Time.now().mjd
params = {"target": "", "file-types": "HDF5", "time-start": now - 365}
response = requests.get(f"{API}/query-files", params=params).json()
if response["result"] != "success":
    print(response, file=sys.stderr)
    raise IOError("API failure")

# At most 5 gig in size
data = [x for x in response["data"] if x["size"] <= MAX_FILE_GIGS * GIGABYTE]

# Drop the 0001.h5, those are high-time-resolution / low-frequency-resolution
data = [x for x in data if not x["url"].endswith("0001.h5")]

# Sort by most recent first
data.sort(key=lambda x: -x["mjd"])
data = data[:NUM_FILES]

# Download things
for entry in data:
    url = entry["url"]
    size = entry["size"]
    fname = url.split("/")[-1]
    dest = os.path.join(DATA_DIR, fname)
    print(entry)
    if os.path.exists(dest):
        if os.path.getsize(dest) == size:
            print(dest, "already exists")
            continue
        else:
            print(dest, "has weird size??")
    check_disk_space(size)
    print("downloading", dest)
    urlretrieve(url, dest)

with open(os.path.join(DATA_DIR, "index.json"), "w") as f:
    f.write(json.dumps(data, sort_keys=True, indent=2))
