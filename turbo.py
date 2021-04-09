#!/usr/bin/env python

import time

from turbo_seti.find_doppler.find_doppler import FindDoppler

file = (
    "spliced_blc4041424344454647_guppi_59103_04780_DIAG_HIP95802_0019.rawspec.0002.h5"
)

doppler = FindDoppler(
    "data/" + file,
    max_drift=4,  # Max drift rate = 4 Hz/second
    snr=10,  # Minimum signal to noise ratio = 10:1
    out_dir="output",  # This is where the turboSETI output files will be stored.
    gpu_backend=True,
)
start = time.time()
doppler.search()
elapsed = time.time() - start
print(f"turboseti time elapsed: {elapsed:.2f}s")
