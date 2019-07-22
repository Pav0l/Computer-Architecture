#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *


if len(sys.argv) < 2:
    print("Missing CLI argument. Try something like: 'python ls8/ls8.py examples/print8.ls8'")
elif sys.argv[0] == "ls8/ls8.py":
    cpu = CPU()

    cpu.load(sys.argv[1])
    cpu.run()
else:
    print("Unknown file. Try running 'python ls8/ls8.py arg', where arg is path to file with instructions")
