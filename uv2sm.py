#!/usr/bin/env python
"""
Convert a .uvh5 file to a casa .sm file

See:
  https://pyuvdata.readthedocs.io/en/latest/uvdata_tutorial.html
"""

from pyuvdata import UVData

assert __name__ == "__main__"

INPUT_FILENAME = "/home/lacker/julia/Rawx.jl/test/blk2.uvh5"
OUTPUT_FILENAME = "/home/lacker/mkdata/imaging/blk2.ms"

uvd = UVData()
uvd.read(INPUT_FILENAME)

uvd.write_ms(OUTPUT_FILENAME, clobber=True)
