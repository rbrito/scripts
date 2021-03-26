#!/usr/bin/python3

import argparse
import sys

from PIL import Image, ImageDraw

from ocrmypdf.leptonica import Pix
from tqdm import tqdm

WHITE = "#fff"
BLACK = "#000"


# Method taken from jbig2enc, which uses leptonica's pixThresholdToBinary
# function on a PIX.
def threshold_image(in_im, threshold=188, negated=False):
    '''
    in_im (should be) a grayscale PIL.Image. The returned image is a B/W
    PIL.image.

    The threshold value was taken from jbig2enc too.

    **Notice:** 255 is black, 0 is white.
    '''
    #
    # Longhand version of the lambdas:
    #
    # | shorthand                       | Longhand                    |
    # +---------------------------------+-----------------------------+
    # | p > threshold and 255           | 255 if p > threshold else 0 |
    # | 255 - (p > threshold and 255)   | 0 if p <= thresold else 255 |
    # | (p <= threshold) * 255          | 0 if p <= thresold else 255 |

    if not negated:
        effective_filter = lambda p: 0 if p <= threshold else 255
    else:
        effective_filter = lambda p: 255 if p <= threshold else 0

    return in_im.convert('L').point(effective_filter).convert('1', dither=None)


def deskew(im):
    '''
    The returned image is deskewed as done in leptonica.
    '''
    return Pix.frompil(im).deskew().topil()


def despeckle(im, size=2):
    '''
    The returned image is despecled with size 2 or 3.
    '''
    return Pix.frompil(im).despeckle(size).topil()


def wipe_borders(in_file, out_file, wipe_borders=True, border_width=None,
                 to_deskew=False, to_despeckle=False, dpi=None, negated=False):
    # print(f'  *** Options set: {wipe_borders=}, {border_width=},'
    #       ' {to_despeckle=}, {to_deskew=}, {dpi=}, {negated=}')
    with Image.open(in_file) as im:

        if dpi is None:
            try:
                xdpi, ydpi = im.info['dpi']

                # We only want to deal with images that have the same DPIs
                # vertically and horizontally.
                assert xdpi == ydpi

                dpi = xdpi
            except KeyError:
                print(f'The input file {in_file} does not contain its DPI.'
                      ' Please use the --dpi switch.')
                sys.exit(1)

        if wipe_borders:
            draw = ImageDraw.Draw(im)

            if border_width:
                border = border_width
            else:
                border = dpi / 10  # hunch

            fill_color = WHITE if not negated else BLACK

            # FIXME: Does the interpretation of top, left, bottom and right
            # remain the same if the origin is moved from top-left to bottom-left?
            draw.rectangle([0, 0, im.width, border], fill=fill_color)  # top
            draw.rectangle([0, im.height - border, im.width, im.height], fill=fill_color)  # bottom

            # If not desired, comment these
            draw.rectangle([0, 0, border, im.height], fill=fill_color)  # left
            draw.rectangle([im.width - border, 0, im.width, im.height], fill=fill_color)  # right

        # This sucks so much and should be rewritten with context managers
        if to_despeckle:
            despeckled = despeckle(im, threshold_image(im, negated=negated))
        else:
            despeckled = threshold_image(im, negated=negated)

        if to_deskew:
            deskewed = deskew(despeckled)
        else:
            deskewed = despeckled

        deskewed.save(out_file, dpi=(dpi, dpi), resolution=dpi, compression='group4')
        if to_deskew:
            deskewed.close()
        despeckled.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tweak scanned images to bind as PDFs or DJVUs.')

    parser.add_argument('--deskew', action='store_true', default=True,
                        help='deskew the images. (Default: True)')
    parser.add_argument('--despeckle', action='store_true', default=False,
                        help='despeckle the images. (Default: False)')
    parser.add_argument('--dpi', default=None,
                        help='set the DPI of files to process.'
                        ' Only needed if the file doesn\'t have resolution indicated (e.g., pbm).'
                        ' Automatically detected if possible.'
                        ' (Default: guess from input otherwise, None)',
                        type=int)
    parser.add_argument('--border-width', default=False, type=int,
                        help='width of border to blank. (Default: dpi/10)')
    parser.add_argument('--wipe-borders', action='store_true', default=True,
                        help='blank the border of the pages. (Default: True)')
    parser.add_argument('--negated', action='store_true', default=False,
                        help='negate the images to treat inverted images. (Default: False)')
    parser.add_argument('filename', nargs='+',
                        help='name of the file(s) to process')

    args = parser.parse_args()

    for in_file in tqdm(args.filename):
        wipe_borders(in_file, in_file + '.new.tif',
                     wipe_borders=args.wipe_borders,
                     border_width=args.border_width,
                     to_deskew=args.deskew,
                     to_despeckle=args.despeckle,
                     dpi=args.dpi,
                     negated=args.negated
                     )
