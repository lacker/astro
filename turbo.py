#!/usr/bin/env python

import json
import os
import time

from turbo_seti.find_doppler.find_doppler import FindDoppler

DATA_DIR = "/d/astrodata"

with open(os.path.join(DATA_DIR, "index.json")) as f:
    index = json.load(f)

files = [entry["url"].split("/")[-1] for entry in index]

for fname in files:
    print("analyzing", fname)
    doppler = FindDoppler(
        os.path.join(DATA_DIR, fname),
        min_drift=0.001,
        max_drift=4,
        snr=10,
        out_dir=os.path.join(DATA_DIR, "output"),
        gpu_backend=True,
    )
    start = time.time()
    doppler.search()
    elapsed = time.time() - start
    print(f"time to turboseti {fname}: {elapsed:.2f}s")
