#!/usr/bin/env python

import json
import re

def parse_headers(lines):
    """
    Parse 'comment' lines.

    Returns a tuple with the length of the disc in seconds followed by the
    start positions of the tracks in frames (that is, 1/75ths of seconds).
    """

    # Metadata to take from the file
    disc_data = {
        'artist': '',
        'genre': '',
        'length': 0,
        'offsets': [],
        'title': '',
        'year': 0,
        'tracktitles': []
    }

    # This doesn't actually match comments only at the beginning (yet)
    header_lines = [line for line in lines if line != '' and line.startswith('#')]
    other_lines = [line for line in lines if line != '' and not line.startswith('#')]

    # Data from the header
    for line in header_lines:
        m = re.match('^#\s+Track frame offsets:', line)
        if m:
            continue

        m = re.match('^#\s+(\d+)', line)
        if m:
            disc_data['offsets'].append(int(m.group(1)))
            continue

        m = re.match('^#\s+Disc length: (\d+)', line)
        if m:
            disc_data['length'] = int(m.group(1))
            disc_data['offsets'].append(int(m.group(1)) * 75)
            break

    # Data from the rest of the file
    for line in other_lines:
        m = re.match('^DTITLE=(.*)\s/\s(.*)', line)
        if m:
            disc_data['artist'] = m.group(1)
            disc_data['title'] = m.group(2)
            break

    for line in other_lines:
        m = re.match('^DYEAR=(\d+)', line)
        if m:
            disc_data['year'] = int(m.group(1))
            break

    for line in other_lines:
        m = re.match('^DGENRE=(.*)', line)
        if m:
            disc_data['genre'] = m.group(1)
            break

    for line in other_lines:
        m = re.match('^TTITLE(\d+)=(.*)', line)
        if m:
            disc_data['tracktitles'].append(m.group(2))

    return disc_data


if __name__ == '__main__':

    with open('example.cddb') as f:
        lines = f.readlines()

    # seconds, frames = parse_headers(lines)
    # print('The disc has %d seconds.' % seconds)
    # print('The tracks begin: %s.' % frames[:-1])
    # print('The tracks delim: %s.' % frames)

    data = parse_headers(lines)
    print json.dumps(data, indent=4)
