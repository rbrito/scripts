#!/usr/bin/env python

from __future__ import print_function

import re

s = open('sicp-split-points.txt').readlines()

def f(s):
    # res = filter(lambda x: x != '', re.split(r"[: ,\n]", s))
    res = [x for x in re.split(r"[: ,\n]", s) if x != '']
    res2 = [res[0]]
    #res2.extend(map(int, res[1:]))
    res2.extend(list(map(int, res[1:])))
    return res2


foos = [f(x) for x in s]

#ffmpeg_opts = "-map_metadata -1 -vf hqdn3d=7:7:5:5 -crf 25 -c:a libfdk_aac -b:a 48k"

ffmpeg_opts ={'avi': '-map_metadata -1 -c copy',
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
            print("ffmpeg -i %s.avi %s -ss %d -to %d %s-%d.%s" %
                  (name, ffmpeg_opts[ext], l[i], l[i+1], name, i+1, ext))
        else:
            print("ffmpeg -ss %d -i %s.avi %s %s-%d.%s" %
                  (l[i], name, ffmpeg_opts[ext], name, i+1, ext))
