#!/usr/bin/env python3

from datetime import datetime
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
        self.rawdata = self.raw.split(".")[1]
        self.length_in_blocks = int(self.length / SECS_PER_BLOCK)
        self.nice_time = datetime.fromtimestamp(self.output_time).strftime("%D %T")

    def timing_info(self):
        "Information about all rows with this timing."
        return f"{self.output_time} {self.nice_time} {self.target:>14} {int(self.length):4} ({self.length_in_blocks:5})"

    def percent(self):
        "Percent completion for just this row."
        # TODO: it seems like either "start_time" or "leftover_blocks" is misnamed here.
        leftover_blocks = self.start_time / BLOCK_SIZE
        rawdata_blocks = 128 * int(self.rawdata, base=10) + leftover_blocks
        percent = int(100 * rawdata_blocks / self.length_in_blocks)
        return percent


with open(full_path) as file:
    machine_set = set()

    # rowmap[timing][machine] lets you look up a row by its timing and machine
    rowmap = {}

    for line in file:
        row = Row(line)
        if row.timing not in rowmap:
            rowmap[row.timing] = {}
        rowmap[row.timing][row.machine] = row
        machine_set.add(row.machine)

    machines = sorted(machine_set)
    print(
        f"#                                                        :  {'  '.join(machine[-2:] for machine in machines)}  "
    )
    for timing in sorted(rowmap.keys()):
        entries = []
        timing_info = None
        scan = None
        for machine in machines:
            if machine not in rowmap[timing]:
                entries.append("---")
            else:
                row = rowmap[timing][machine]
                if not timing_info:
                    timing_info = row.timing_info()
                    scan = row.scan
                entries.append(f"{row.percent():>3}")
        print(f"{timing_info} : {' '.join(entries)}   {scan}")
