#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dateutil.parser
import sys

# Info about files that we want to concatenate:
#     mediainfo --Inform="file:///tmp/chap_template.txt" *.mp4 > input.txt
# Contents of chap_template.txt:
#     General;%FileName%\n%Duration/String3%\n

# FIXME: Kludge, as I can't seem to get everyting normalized in UTC
EPOCH = dateutil.parser.parse('1970-01-01T00:00:00 UTC').strftime('%s.%f')

def time_to_timestamp(s):
    return dateutil.parser.parse('1970-01-01T%s UTC' % s).strftime('%s.%f')

def main():
    L = sys.stdin.readlines()
    L = [l.strip() for l in L if l.strip() != '']  # redundant

    L.pop()  # remove the last timestamp, as that's not used
    L.insert(0, '00:00:00.000')  # insert the time to be used as basis

    for i in range(0, len(L), 2):
        print 'CHAPTER%02d=%s' % (i/2 + 1, L[i])
        print 'CHAPTER%02dNAME=%s' % (i/2+1, L[i+1])

main()
