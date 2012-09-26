#!/usr/bin/env python

for j in [16, 8, 4, 2]:
    print "mod ", j
    for i in range(1, 1000):
        h = i*j
        if h % 9 == 0:
            print "*", h*16/9, "x", h
