#!/usr/bin/env python

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


def analyze(fname):
    dat_path = os.path.join(OUTPUT_DIR, fname.rsplit(".", 1)[0] + ".dat")
    if not os.path.exists(dat_path):
        with tempfile.TemporaryDirectory() as tmp_dir:
            print("analyzing", fname)
            doppler = FindDoppler(
                os.path.join(DATA_DIR, fname),
                min_drift=0.001,
                max_drift=4,
                snr=10,
                out_dir=tmp_dir,
                gpu_backend=True,
                n_coarse_chan=N_COARSE_CHAN.get(fname),
            )
            start = time.time()
            doppler.search()
            elapsed = time.time() - start
            print(f"time to turboseti {fname}: {elapsed:.2f}s")
            copy_tree(tmp_dir, OUTPUT_DIR)

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
