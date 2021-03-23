#!/usr/bin/python3

import sys

from PIL import Image, ImageDraw

from ocrmypdf.leptonica import Pix
from tqdm import tqdm

WHITE = "#fff"


# Method taken from jbig2enc, which uses leptonica's pixThresholdToBinary
# function on a PIX.
def threshold_image(in_im, threshold=188):
    '''
    in_im (should be) a grayscale PIL.Image. The returned image is a B/W
    PIL.image.

    The threshold value was taken from jbig2enc too.
    '''
    return in_im.convert('L').point(lambda p: p > threshold and 255).convert('1', dither=None)


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


def wipe_borders(in_file, out_file):
    with Image.open(in_file) as im:

        xdpi, ydpi = im.info['dpi']

        # We only want to deal with images that have the same DPIs
        # vertically and horizontally.
        assert xdpi == ydpi

        dpi = xdpi
        border = dpi / 10  # hunch

        draw = ImageDraw.Draw(im)

        # FIXME: Does the interpretation of top, left, bottom and right
        # remain the same if the origin is moved from top-left to bottom-left?
        draw.rectangle([0, 0, im.width, border], fill=WHITE)  # top
        draw.rectangle([0, im.height - border, im.width, im.height], fill=WHITE)  # bottom

        # If not desired, comment these
        draw.rectangle([0, 0, border, im.height], fill=WHITE)  # left
        draw.rectangle([im.width - border, 0, im.width, im.height], fill=WHITE)  # right

        despeckled = threshold_image(im)
        deskewed = deskew(despeckled)

        # deskewed = deskew(threshold_image(im))
        # im.save(out_file, dpi=(DPI, DPI), resolution=DPI, compression="packbits")  # for PNGs: compress_level=1

        deskewed.save(out_file, dpi=(dpi, dpi), resolution=dpi, compression='group4')
        deskewed.close()
        # despeckled.save(out_file, dpi=(DPI, DPI), resolution=DPI, compression='group4')
        despeckled.close()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Usage: %s image [image ...]' % sys.argv[0])
        sys.exit(1)

    for in_file in tqdm(sys.argv[1:]):
        # print('Processing <%s>.' % in_file)
        wipe_borders(in_file, in_file + '.new.tif')
