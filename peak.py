#!/usr/bin/env python

import cupy as cp

if __name__ == "__main__":
    data = cp.random.rand(100, 100)
    data[10, 20] = 30
    data[40, 50] = 60
    data[70, 80] = 90
