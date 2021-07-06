#!/usr/bin/env python
"""
Tools to inspect an h5 file with some radio telescope readings.
These files are mostly nothingness plus quiet noise, so to inspect them,
we need to be figuring out where the interesting areas are.
"""
import hdf5plugin
import h5py
import cupy

EXAMPLE_FILE = "data/blc41_guppi_59103_01372_PSR_B2021+51_0009.rawspec.0000.h5"


class Viewer(object):
    pass
