#!/usr/bin/env python3

from __future__ import print_function

import re
import sys


def usage():
    print("%s <filename>" % sys.argv[0])


def main():
    x = 1000000000000000 # infinity
    y = 1000000000000000 # infinity
    w = -1000000000000000 # - infinity
    h = -1000000000000000 # - infinity

    # FIXME: Generalize to loop over multiple files
    with open(sys.argv[1]) as input_file:
        lines = input_file.readlines()

    for line in lines:
        m = re.match(r'%%BoundingBox: (\d+) (\d+) (\d+) (\d+)', line)
        if not m:
            continue

        x_cur = int(m.group(1))
        y_cur = int(m.group(2))
        w_cur = int(m.group(3))
        h_cur = int(m.group(4))

        if x_cur < x:
            x = x_cur
        if y_cur < y:
            y = y_cur

        if w_cur > w:
            w = w_cur
        if h_cur > h:
            h = h_cur

    print('--bbox "%d %d %d %d"' % (x, y, w, h))


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        usage()
        sys.exit(1)

    main()
