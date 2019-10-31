#!/usr/bin/env python3

import re
import sys
import argparse


def update_bbox(x_cur, y_cur, w_cur, h_cur, x, y, w, h):
    x = x_cur if x_cur < x else x
    y = y_cur if y_cur < y else y

    w = w_cur if w_cur > w else w
    h = h_cur if h_cur > h else h

    return x, y, w, h

def main(args):
    x = 1000000000000000 # infinity
    y = 1000000000000000 # infinity
    w = -1000000000000000 # - infinity
    h = -1000000000000000 # - infinity

    all_parities = (args.even == False) and (args.odd == False)
    selected_parity = int(0 if args.even else args.odd)

    # FIXME: Generalize to loop over multiple files
    with open(args.filename) as input_file:
        lines = input_file.readlines()

    for line in lines:
        m = re.match(r'\* Page (\d+): (\d+) (\d+) (\d+) (\d+)', line)
        if not m:
            continue

        page  = int(m.group(1))
        x_cur = int(m.group(2))
        y_cur = int(m.group(3))
        w_cur = int(m.group(4))
        h_cur = int(m.group(5))

        # Ghostscript found and empty BBox; we skip regardless of the parity
        if (x_cur, y_cur, w_cur, h_cur) == (0, 0, 0, 0):
            continue

        # We compute the coordinates corresponding only to the pages of the
        # parity given (this way, we avoid even more duplicate code).
        if not all_parities:
            if page % 2 == selected_parity:
                x, y, w, h = update_bbox(x_cur, y_cur, w_cur, h_cur, x, y, w, h)
        else:
            x, y, w, h = update_bbox(x_cur, y_cur, w_cur, h_cur, x, y, w, h)

    # FIXME: This code can be much, much more compact (we have to eliminate
    # redundancies).
    if all_parities:
        print('--bbox ', end='')
    else:
        if selected_parity == 0:
            print('--bbox-even ', end='')
        else:
            print('--bbox-odd ', end='')

    print('"%d %d %d %d"' % (x, y, w, h))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find bounding boxes for PDF files')

    parser.add_argument('--odd', action='store_true', default=False,
                        help='compute the boxes only for odd pages')
    parser.add_argument('--even', action='store_true', default=False,
                        help='compute the boxes only for even pages')
    parser.add_argument('filename',
                        help='name of the file to compute the bounding box for')

    args = parser.parse_args()

    if args.odd and args.even:
        print('--odd is mutually exclusive with --even')
        sys.exit(1)

    main(args)
