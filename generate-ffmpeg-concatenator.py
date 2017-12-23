#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
We will generate a line like the following (copied from
https://trac.ffmpeg.org/wiki/Concatenate#Instructions2 and slightly edited):

ffmpeg -i input1.mp4 -i input2.webm -i input3.mov \
-filter_complex "[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[outv][outa]" \
-map "[outv]" -map "[outa]" output.mkv
"""

import sys


def generate_inputs(input_files):
    """
    Generate list of inputs to ffmpeg, with the -i option before each file name.
    """
    inputs = []

    for input_file in input_files:
        inputs.extend(['-i', input_file])

    return inputs


def generate_filter(input_files):
    """
    Generate list of inputs to ffmpeg, with the -i option before each file name.
    """
    cmd_filter = ['-filter_complex']

    filter_string_parts = []  # this will be joined to become a single string

    n = len(input_files)
    for i in range(n):
        filter_string_parts.append('[%d:v:0][%d:a:0]' % (i, i))

    filter_string_parts.append('concat=n=%d:v=1:a=1[outv][outa]' % (n))

    filter_string = ''.join(filter_string_parts)
    cmd_filter.append(filter_string)

    return cmd_filter


if __name__ == '__main__':
    cmd_part0 = ['ffmpeg']

    cmd_inputs = generate_inputs(sys.argv[1:])
    cmd_filter = generate_filter(sys.argv[1:])

    cmd_trailing = ['-map', '[outv]', '-map', '[outa]', 'output.mkv']

    cmd_final = cmd_part0 + cmd_inputs + cmd_filter + cmd_trailing

    print(cmd_final)
