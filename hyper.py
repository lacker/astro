#!/usr/bin/env python

from hyperseti import hyperseti

fname = "data/blc41_guppi_59103_01372_PSR_B2021+51_0009.rawspec.0000.h5"

hits = hyperseti.find_et_serial(
    fname, filename_out="output/hits.csv", max_dd=1.0, threshold=50
)
