#!/usr/bin/python3

import re
import sys

lines = sys.stdin.readlines()

for lineno, line in enumerate(lines):
    m = re.match(r'(?P<hours>\d+:)?(?P<minutes>\d+):(?P<seconds>\d+)(?:\.(?P<millis>\d+))\s+(?P<title>.*)', line)
    if m:
        parts = m.groupdict()
        if parts['hours']:
            hours = int(parts['hours'].replace(':', '')) # clean with better regexp
        else:
            hours = 0
        minutes = int(parts['minutes'])
        seconds = int(parts['seconds'])
        if parts['millis']:
            millis = int(parts['millis'])
        else:
            millis = 0

        print('CHAPTER%02d=%02d:%02d:%02d.%03d' % (lineno, hours, minutes, seconds, millis))
        print('CHAPTER%02dNAME=%s' % (lineno, parts['title']))
    else:
        m = re.match(r'(?P<title>.*?)\s+(?P<hours>\d+:)?(?P<minutes>\d+):(?P<seconds>\d+)(:\.(?P<millis>)?', line)
        # Code repetition, ugh!
        if m:
            parts = m.groupdict()
            if parts['hours']:
                hours = int(parts['hours'].replace(':', '')) # clean with better regexp
            else:
                hours = 0
            minutes = int(parts['minutes'])
            seconds = int(parts['seconds'])
            if parts['millis']:
                millis = int(parts['millis'])
            else:
                millis = 0

            print('CHAPTER%02d=%02d:%02d:%02d.%03d' % (lineno, hours, minutes, seconds, millis))
            print('CHAPTER%02dNAME=%s' % (lineno, parts['title']))
