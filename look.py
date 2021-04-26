#!/usr/bin/env python

# FILE = "/d/astrodata/guppi_59012_80282_6072999122_XaS038-S5-HVS_R_0001.0000.h5"
FILE = "/d/astrodata/guppi_59012_79941_6072997821_XaS038-S5-HVS_S_0001.0000.h5"
from blimpy import Waterfall

obs = Waterfall(FILE)
print(obs.info())
