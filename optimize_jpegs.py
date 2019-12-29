#!/usr/bin/env python3

import logging
import os.path
import subprocess
import sys
import tempfile

import pikepdf


def main(tmpdirname, my_pdf):
    my_pdf = pikepdf.open(sys.argv[1])

    for obj in my_pdf.objects:

        # Not elegant, but (hopefully) will be made so in the near future
        if isinstance(obj, pikepdf.Stream) and '/Subtype' in obj and obj['/Subtype'] == '/Image':
            image_obj = obj

            if '/Filter' not in image_obj:
                continue

            # FIXME: to improve *a lot*
            if (image_obj.Filter != '/DCTDecode' and
               not (isinstance(image_obj.Filter, pikepdf.Array) and
                    len(image_obj.Filter) == 1 and
                    image_obj.Filter[0] == '/DCTDecode')):
                continue

            if image_obj.ColorSpace not in ('/DeviceRGB', '/DeviceGray'):
                continue

            logging.debug('Found a JPEG as %s', image_obj.ColorSpace)

            tempname = os.path.join(tmpdirname, 'foobarbaz.jpg')  # FIXME: change this
            source = open(tempname, 'wb')

            ret = source.write(image_obj.read_raw_bytes())
            logging.info('Wrote %d bytes to the tempfile %s.', ret, tempname)
            source.close()

            # print('Calling jpgcrush...')
            ret = subprocess.call(['jpgcrush', tempname])
            # print('Return code was: %d.' % ret)

            # Unfortunatel, the -purejpg of jhead is too aggressive and may
            # strip way too much to the point of modifying the image, in some
            # cases.
            logging.info('Calling jhead...')
            ret = subprocess.call(['jhead', '-dt', '-dc', '-de', source.name])
            # print('Return code was: %d.' % ret)

            targetfn = open(tempname, 'rb')
            target = targetfn.read()
            logging.info('Read back %d bytes from the tempfile.', len(target))
            image_obj.write(target, filter=pikepdf.Name('/DCTDecode'))
            logging.info('The image is back on the PDF file.')

    logging.debug('going to save the file')
    my_pdf.save(os.path.splitext(sys.argv[1])[0] + '.jpg.pdf')

    my_pdf.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmpdirname:
        logging.debug('    **** Temporary directory created: %s', tmpdirname)
        os.environ['TMPDIR'] = tmpdirname
        main(tmpdirname, sys.argv[1])
