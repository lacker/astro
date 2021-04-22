#!/usr/bin/env python

FILE = "/d/astrodata/guppi_59012_80282_6072999122_XaS038-S5-HVS_R_0001.0000.h5"

from blimpy import Waterfall

data = Waterfall(FILE)
print(data.info())
