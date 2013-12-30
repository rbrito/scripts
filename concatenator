#!/usr/bin/env python

import fnmatch
import os
import subprocess

EXT = 'flv'

OFFSET = 3

os.system("mediainfo --Inform='General;%Duration/String3%\\n%FileName%\\n'"
          " *." + EXT + " | ~/src/utils/simplechaps.py > chaps.txt")

our_basename = os.path.basename(os.path.realpath('.'))

dir_entries = os.walk('.').next()

our_files = sorted(fnmatch.filter(dir_entries[2], '*.' + EXT))


parameters = ['mkvmerge',
              '--chapters', 'chaps.txt',
              '-o', '../%s.mkv' % our_basename,
              ]

parameters.append(our_files[0])
for f in our_files[1:]:
    parameters.append('+')
    parameters.append(f)

print parameters

subprocess.call(parameters)
