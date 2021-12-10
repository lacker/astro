#!/usr/bin/env python

from blimpy.io.hdf_reader import H5Reader
from distutils.dir_util import copy_tree
import json
import os
import sys
import tempfile
import time

from turbo_seti.find_doppler.find_doppler import FindDoppler

DATA_DIR = "/d/astrodata"
OUTPUT_DIR = os.path.join(DATA_DIR, "output")

N_COARSE_CHAN = {"guppi_59012_80282_6072999122_XaS038-S5-HVS_R_0001.0000.h5": 16}


def find_doppler(fname):
    # Do our own coarse channel counting heuristics
    fpath = os.path.join(DATA_DIR, fname)
    header = H5Reader(fpath, load_data=False).read_header()
    nchans = header["nchans"]
    if nchans == 64000000 and fname.endswith("0000.h5"):
        # According to davidm this means this is Parkes UWL single node, so 1 coarse channel.
        # We can't process that much at once, though, so we use a higher number for batching.
        n_coarse_chan = 16
    else:
        # Use default n_coarse_chan heuristics
        n_coarse_chan = None

    with tempfile.TemporaryDirectory() as tmp_dir:
        print("analyzing", fname)
        doppler = FindDoppler(
            fpath,
            min_drift=0.001,
            max_drift=4,
            snr=10,
            out_dir=tmp_dir,
            gpu_backend=True,
            n_coarse_chan=n_coarse_chan,
        )
        start = time.time()
        doppler.search()
        elapsed = time.time() - start
        print(f"time to turboseti {fname}: {elapsed:.2f}s")
        copy_tree(tmp_dir, OUTPUT_DIR)


def analyze(fname):
    dat_path = os.path.join(OUTPUT_DIR, fname.rsplit(".", 1)[0] + ".dat")
    if not os.path.exists(dat_path):
        find_doppler(fname)

    if not os.path.exists(dat_path):
        raise IOError(f"turboseti did not generate dat as expected at {dat_path}")

    with open(dat_path) as f:
        lines = f.readlines()
        assert lines[0].startswith("# ---------------------")
        assert lines[1].startswith("# File ID:")
        assert lines[2].startswith("# ---------------------")
        assert lines[3].startswith("# Source:")
        assert lines[4].startswith("# MJD:")
        assert lines[5].startswith("# DELTAT:")
        assert lines[6].startswith("# ---------------------")
        assert lines[7].startswith("# Top_Hit_#")
        assert lines[8].startswith("# ---------------------")
        hits = lines[9:]
        return hits


def process_files(files):
    hits = []
    for fname in files:
        for hit in analyze(fname):
            hits.append((hit, fname))

    print(len(hits), "hits:")
    for hit, fname in hits:
        print(f"from {fname}:")
        print(f"  {hit}")


def process_all():
    with open(os.path.join(DATA_DIR, "index.json")) as f:
        index = json.load(f)

    files = [entry["url"].split("/")[-1] for entry in index]
    process_files(files)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        process_all()
    else:
        files = sys.argv[1:]
        print("processing:", " ".join(files))
        process_files(files)
