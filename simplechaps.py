#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dateutil.parser
import sys

# Info about files that we want to concatenate:
#     mediainfo --Inform="file:///tmp/chap_template.txt" *.mp4 > input.txt
# Contents of chap_template.txt:
#     General;%FileName%\n%Duration/String3%\n

def time_to_timestamp(stamp):
    return dateutil.parser.parse('1970-01-01T%s UTC' % stamp).strftime('%s.%f')

# Kludge, as I can't seem to get everyting normalized in UTC
EPOCH = time_to_timestamp('00:00:00')


def main():
    lines = sys.stdin.readlines()
    lines = [line.strip() for line in lines if line.strip() != '']  # redundant

    lines.pop()  # remove the last timestamp, as that's not used
    lines.insert(0, '00:00:00.000')  # insert the time to be used as basis

    for i in range(0, len(lines), 2):
        print 'CHAPTER%02d=%s' % (i/2 + 1, lines[i])
        print 'CHAPTER%02dNAME=%s' % (i/2 + 1, lines[i+1])

if __name__ == '__main__':
    main()
