#!/usr/bin/env python3

import os
import sys

# TODO: change before sticking on telescope cluster
BASE_DIR = "/home/lacker/obs/target_logs"
BLOCK_SIZE = 134224384
SECS_PER_BLOCK = 0.17899


if len(sys.argv) < 2:
    print("usage: parse_obs_log.py <session>", file=sys.stderr)
    sys.exit(1)

session = sys.argv[1]
full_path = os.path.join(BASE_DIR, session)
if not os.path.exists(full_path):
    print(f"file does not exist: {full_path}", file=sys.stderr)
    sys.exit(1)


class Row:
    """
    Structured data generated from one line of the input.
    """

    def __init__(self, line):
        parts = line.strip().split()
        if len(parts) != 7:
            raise ValueError(f"could not parse line: {line}")
        self.machine, session_copy, self.target, self.raw, start_time, num_bytes, length = (
            parts
        )
        if session != session_copy:
            raise ValueError(f"session mismatch: {session} != {session_copy}")
        self.start_time = int(start_time)
        self.num_bytes = int(num_bytes)
        self.length = float(length)
        self.timing = self.raw.split("/")[-1][:17]
        _, mjd, mjd_secs = self.timing.split("_")
        self.output_time = (int(mjd) - 40587) * 86400 + int(mjd_secs)
        self.scan = self.raw.split("/")[-1].split(".")[0].split("_")[-1]
        self.length_in_blocks = int(self.length / SECS_PER_BLOCK)
        # TODO: nicedate logic


with open(full_path) as file:
    for line in file:
        row = Row(line)
        print(row.scan, row.length, row.length_in_blocks, row.output_time)
        raise Exception("XXX")
