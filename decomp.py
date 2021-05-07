#!/usr/bin/env python

from blimpy import Waterfall
import h5py

# BASE = "data/blc41_guppi_59103_01372_PSR_B2021+51_0009.rawspec.0000"
BASE = "../VoyagerTutorialRepository/voyager_2020_data/single_coarse_guppi_59046_80036_DIAG_VOYAGER-1_0011.rawspec.0000"

H5 = BASE + ".h5"
DAT = BASE + ".dat"

h5 = h5py.File(H5, mode="r")
print(list(h5.keys()))

# waterfall = Waterfall(H5)
# print(waterfall.info())
