#!/usr/bin/python3

import re
import sys

lines = sys.stdin.readlines()

for lineno, line in enumerate(lines):
    m = re.match(r'(?P<hours>\d+:)?(?P<minutes>\d+):(?P<seconds>\d+) (?P<title>.*)', line)
    if m:
        parts = m.groupdict()
        if parts['hours']:
            hours = int(parts['hours'].replace(':', '')) # clean with better regexp
        else:
            hours = 0
        minutes = int(parts['minutes'])
        seconds = int(parts['seconds'])
        # print(hours)
        # print(minutes)
        # print(seconds)
        
        print('CHAPTER%02d=%02d:%02d:%02d.000' % (lineno, hours, minutes, seconds))
        print('CHAPTER%02dNAME=%s' % (lineno, parts['title']))
