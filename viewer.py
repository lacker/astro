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
    def __init__(self, filename):
        self.h5file = h5py.File(filename, mode="r")
        self.data = self.h5file["data"]
        self.height, one, self.width = self.data.shape
        assert one == 1

        print("loading data onto the GPU...")
        self.array = cupy.asarray(self.data[:, 0, :])


if __name__ == "__main__":
    v = Viewer(EXAMPLE_FILE)
    print("data is", v.height, "x", v.width)
    mean = cupy.mean(v.array)
    print("mean is", mean)
    std = cupy.std(v.array)
    print("std is", std)
    k = 2
    threshold = mean + k * std
    print("using threshold", threshold)
    m = cupy.max(v.array, axis=0)
    print(m.shape)
    print((m > threshold).sum(), f"columns have data beyond +{k} stdev")

    chunks = 64
    assert len(m) % chunks == 0
    chunk_size = len(m) // chunks

    for i in range(chunks):
        print("analyzing chunk", i)
        chunk = v.array[:, i * chunk_size : (i + 1) * chunk_size]
        print("chunk size is", chunk.shape)
        chunk_mid = chunk.shape[1] // 2
        print("max of chunk left for chunk", i, "is", cupy.max(chunk[:, :chunk_mid]))
        print(
            "max of chunk right for chunk",
            i,
            "is",
            cupy.max(chunk[:, (chunk_mid + 1) :]),
        )
