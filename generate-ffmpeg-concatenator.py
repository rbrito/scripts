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


def generate_filter(num_files):
    """
    Generate list of mappings for the -filter_complex option of ffmpeg.

    Example:
    >>> generate_filter(3)
    ['-filter_complex', '[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[outv][outa]']
    """
    cmd_filter = ['-filter_complex']

    filter_string_parts = []  # this will be joined to become a single string

    for i in range(num_files):
        filter_string_parts.append('[%d:v:0][%d:a:0]' % (i, i))

    filter_string_parts.append('concat=n=%d:v=1:a=1[outv][outa]' % (num_files))

    filter_string = ''.join(filter_string_parts)
    cmd_filter.append(filter_string)

    return cmd_filter


def main():
    cmd_part0 = ['ffmpeg']

    cmd_inputs = generate_inputs(sys.argv[1:])
    cmd_filter = generate_filter(len(sys.argv) - 1)

    cmd_trailing = ['-map', '[outv]', '-map', '[outa]', 'output.mkv']

    cmd_final = cmd_part0 + cmd_inputs + cmd_filter + cmd_trailing

    print(cmd_final)


if __name__ == '__main__':
    main()
