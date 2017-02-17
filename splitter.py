#!/usr/bin/env python

from __future__ import print_function

import re

with open('sicp-split-points.txt') as f:
    s = f.readlines()


def f(s):
    res = [x for x in re.split(r"[: ,\n]", s) if x != '']
    return res


foos = [f(x) for x in s]

# ffmpeg_opts = ("-map_metadata -1 -vf hqdn3d=7:7:5:5 -crf 25 "
#                "-c:a libfdk_aac -b:a 48k")

ffmpeg_opts = {'avi': '-map_metadata -1 -c copy',
               'mp4': '-map_metadata -1 -preset ultrafast -crf 25'}

ext = 'mp4'

for foo in foos:
    name = foo[0]
    l = foo[1:]
    n = len(l)
    for i in range(n):
        if i < n-1:
            # peculiarity of ffmpeg: you have to put both the start (-ss)
            # and end (-to) of the video right before the output file name;
            # otherwise, they don't do what we expect them to do.
            print("ffmpeg -i %s.avi %s -ss %s -to %s %s-%d.%s" %
                  (name, ffmpeg_opts[ext], l[i], l[i+1], name, i+1, ext))
        else:
            print("ffmpeg -ss %s -i %s.avi %s %s-%d.%s" %
                  (l[i], name, ffmpeg_opts[ext], name, i+1, ext))
    print()
