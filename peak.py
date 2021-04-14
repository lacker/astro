#!/usr/bin/env python

import cupy as cp
import cupyx.scipy.ndimage
import numpy as np

if __name__ == "__main__":
    data = cp.random.rand(10, 10)
    data[1, 2] = 30
    data[4, 5] = 60
    data[7, 8] = 90

    threshold = 1.0
    # Find maxes
    maxes = cupyx.scipy.ndimage.maximum_filter(data, size=(5, 5))
    # Find peaks
    peaks = cp.logical_and(maxes == data, data >= threshold)
    with np.printoptions(linewidth=200):
        print(maxes)
        print(peaks)
        print(cp.argwhere(peaks))
