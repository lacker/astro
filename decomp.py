#!/usr/bin/env python

import hdf5plugin
import h5py

h5 = h5py.File("data/voyager.h5", mode="r")
data = h5["data"]
print(data[0, 0, 0])
