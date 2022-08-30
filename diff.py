#!/usr/bin/env python

from blimpy import Waterfall
import h5py
import numpy as np
import os


DATA_DIR = os.path.expanduser("~/data/difftest")
H5 = os.path.join(DATA_DIR, "guppi_59816_50605_000017_J1939-6342_0001.band00.beam00.h5")
FIL = os.path.join(DATA_DIR, "guppi_59816_50605_000017_J1939-6342.SB00.B00.fil")


h5 = h5py.File(H5, mode="r")
data = h5["data"]
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
    h5_val = data.attrs[key]
    fil_val = fil.header[key]
    if not approx_equal(h5_val, fil_val):
        print(f"mismatch for {key}:")
        print(f"h5 value: {h5_val}")
        print(f"fil value: {fil_val}")

fil_rows = fil.data.shape[0]
h5_rows = data.shape[0]

# Allow the implementations to differ on the last row, ie truncation policy
if abs(fil_rows - h5_rows) > 1:
    print("shape mismatch:")
    print("fil shape:", fil.data.shape)
    print("h5 shape:", data.shape)

# Check actual data
for row in range(min(fil_rows, h5_rows)):
    fil_row = fil.data[row][0]
    h5_row = data[row][0]
    if len(fil_row) != len(h5_row):
        print(f"row {row} length mismatch:")
        print(f"{len(fil_row)=}")
        print(f"{len(h5_row)=}")
        break
    diffs = (fil_row - h5_row) / fil_row.mean()

    # Allow 1% disagreement for numerical instability
    diff_count = np.count_nonzero(diffs > 0.01)
    if diff_count > 0:
        print(f"row {row} diff: {diff_count}")
    else:
        print(f"row {row} ok")
