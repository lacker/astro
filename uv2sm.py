#!/usr/bin/env python
"""
Convert a .uvh5 file to a casa .sm file

See:
  https://pyuvdata.readthedocs.io/en/latest/uvdata_tutorial.html
"""

import os
from pyuvdata import UVData

assert __name__ == "__main__"

INPUT_FILENAME = os.path.expanduser("~/mkdata/imaging/head.uvh5")
OUTPUT_FILENAME = os.path.expanduser("~/mkdata/imaging/head.ms")

uvd = UVData()
uvd.read(INPUT_FILENAME)

uvd.write_ms(OUTPUT_FILENAME, clobber=True)
