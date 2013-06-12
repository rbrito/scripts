#!/usr/bin/env python

import re

def parse_headers(lines):
    """
    Parse 'comment' lines.

    Returns a tuple with the length of the disc in seconds followed by the
    start positions of the tracks in frames (that is, 1/75ths of seconds).
    """
    offsets = []
    disc_length = 0
    # This doesn't actually match comments only at the beginning (yet)
    lines = [line for line in lines if line != '' and line[0] == '#']
    for line in lines:
        m = re.match('^#\s+Track frame offsets:', line)
        if m:
            continue

        m = re.match('^#\s+(\d+)', line)
        if m:
            offsets.append(int(m.group(1)))
            continue

        m = re.match('^#\s+Disc length: (\d+)', line)
        if m:
            disc_length = int(m.group(1))
            break

    return disc_length, offsets


if __name__ == '__main__':
    f = file('example.cddb')
    lines = f.readlines()
    seconds, frames = parse_headers(lines)
    print('The disc has %d seconds.' % seconds)
    print('The tracks begin at %s frames.' % frames)
