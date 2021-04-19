#!/usr/bin/env python
import random, sys
lines = sys.stdin.readlines()
random.shuffle(lines)
for line in lines:
    print(line, end="")
