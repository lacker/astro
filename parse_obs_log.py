#!/usr/bin/env python3


class Row(object):
    def __init__(self, line):
        parts = line.strip().split()
        if len(parts) != 7:
            raise ValueError("could not parse line: " + line)
