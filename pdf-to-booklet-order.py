#!/usr/bin/env python3

import sys

limit = (int(sys.argv[1])+1)//4 * 4

for i in range(1, limit+1, 4):
    print(f'a{i:03d}.tif')
    print(f'a{i+2:03d}.tif')
    print(f'a{i+1:03d}.tif')
    print(f'a{i+3:03d}.tif')
