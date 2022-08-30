#!/usr/bin/env python

from blimpy import Waterfall
import h5py
import os


DATA_DIR = os.path.expanduser("~/data/difftest")
H5 = os.path.join(DATA_DIR, "guppi_59816_50605_000017_J1939-6342_0001.band00.beam00.h5")
FIL = os.path.join(DATA_DIR, "guppi_59816_50605_000017_J1939-6342.SB00.B00.fil")


h5 = h5py.File(H5, mode="r")
fil = Waterfall(FIL)

def force_decode(s):
    if hasattr(s, "decode"):
        return s.decode()
    return s

def approx_equal(a, b):
    if type(a) is float:
        return abs(a - b) / abs(a) < 0.01
    return force_decode(a) == force_decode(b)

# Check metadata
mismatches = 0
for key in ["fch1", "foff", "source_name", "tsamp", "tstart"]:
    h5_val = h5["data"].attrs[key]
    fil_val = fil.header[key]
    if not approx_equal(h5_val, fil_val):
        if mismatches:
            print()
        mismatches += 1
        print(f"mismatch for {key}:")
        print(f"h5 value: {h5_val}")
        print(f"fil value: {fil_val}")
