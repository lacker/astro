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

NUM_CHUNKS = 64


class Viewer(object):
    def __init__(self, filename):
        self.h5file = h5py.File(filename, mode="r")
        self.data = self.h5file["data"]
        self.height, one, self.width = self.data.shape
        assert one == 1

    def chunk(self, n):
        assert 0 <= n < NUM_CHUNKS
        chunk_size = self.width // NUM_CHUNKS
        return cupy.asarray(self.data[:, 0, n * chunk_size : (n + 1) * chunk_size])


if __name__ == "__main__":
    v = Viewer(EXAMPLE_FILE)
    print("data is", v.height, "x", v.width)

    for i in range(NUM_CHUNKS):
        print("analyzing chunk", i)
        chunk = v.chunk(i)
        print("chunk size is", chunk.shape)
        chunk_mid = chunk.shape[1] // 2
        print("max of chunk left for chunk", i, "is", cupy.max(chunk[:, :chunk_mid]))
        spike_avg = cupy.mean(chunk[:, chunk_mid])
        print("spike avg is", spike_avg)
        print(
            "max of chunk right for chunk",
            i,
            "is",
            cupy.max(chunk[:, (chunk_mid + 1) :]),
        )
