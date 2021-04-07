#!/usr/bin/env python

import time

from turbo_seti.find_doppler.find_doppler import FindDoppler

# file = "single_coarse_guppi_59046_80036_DIAG_VOYAGER-1_0011.rawspec.0000.h5"
file = "blc41_guppi_59103_01372_PSR_B2021+51_0009.rawspec.0000.h5"

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
