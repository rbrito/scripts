#!/usr/bin/env python3

import logging
import os.path
import subprocess
import sys
import tempfile

import pikepdf

# Set the logging level
logging.basicConfig(level=logging.DEBUG)

my_pdf = pikepdf.open(sys.argv[1])

for page in my_pdf.pages:
    for image in page.images.keys():
        image_obj = page.images[image]

        if '/Filter' not in image_obj:
            continue
        if image_obj.Filter != '/DCTDecode':
            continue
        if image_obj.ColorSpace not in ('/DeviceRGB', '/DeviceGray'):
            continue

        logging.debug('Found a JPEG as %s', image_obj.ColorSpace)

        tempname = '/tmp/foobarbaz.jpg'  # FIXME: change this
        source = open(tempname, 'wb')

        ret = source.write(image_obj.read_raw_bytes())
        logging.info('Wrote %d bytes to the tempfile %s.', ret, tempname)
        source.close()

        # print('Calling jpgcrush...')
        ret = subprocess.call(['jpgcrush', tempname])
        # print('Return code was: %d.' % ret)

        logging.info('Calling jhead...')
        ret = subprocess.call(['jhead', '-purejpg', source.name])
        # print('Return code was: %d.' % ret)

        targetfn = open(tempname, 'rb')
        target = targetfn.read()
        logging.info('Read back %d bytes from the tempfile.', len(target))
        image_obj.write(target, filter=pikepdf.Name('/DCTDecode'))
        logging.info('The image is back on the PDF file.')

logging.debug('going to save the file')
my_pdf.save(os.path.splitext(sys.argv[1])[0] + '.jpg.pdf')

my_pdf.close()
