#!/usr/bin/env python

from blimpy import Waterfall
import h5py
import os

assert __name__ == "__main__"

DATA_DIR = os.path.expanduser("~/data/difftest")
H5 = os.path.join(DATA_DIR, "guppi_59816_50605_000017_J1939-6342_0001.band00.beam00.h5")
FIL = os.path.join(DATA_DIR, "guppi_59816_50605_000017_J1939-6342.SB00.B00.fil")


h5 = h5py.File(H5, mode="r")
fil = Waterfall(FIL)

