#!/usr/bin/env python3

import logging
import os.path
import subprocess
import sys
import tempfile

import pikepdf



def main(tmpdirname, pdf_name):
    total_savings = 0

    my_pdf = pikepdf.open(pdf_name)

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

            size_before = source.write(image_obj.read_raw_bytes())
            logging.debug('Wrote %d bytes to the tempfile %s.', size_before, tempname)
            source.close()

            # print('Calling jpgcrush...')
            subprocess.check_call(['jpgcrush', tempname])
            # print('Return code was: %d.' % ret)

            # Unfortunatel, the -purejpg of jhead is too aggressive and may
            # strip way too much to the point of modifying the image, in some
            # cases.
            logging.debug('Calling jhead...')
            subprocess.check_call(['jhead', '-dt', '-dc', '-de', source.name])
            # print('Return code was: %d.' % ret)

            targetfn = open(tempname, 'rb')
            target = targetfn.read()

            size_after = len(target)
            logging.debug('Read back %d bytes from the tempfile %s.', size_after, tempname)
            image_obj.write(target, filter=pikepdf.Name('/DCTDecode'))
            logging.debug('The image is back on the PDF file.')

            total_savings += size_before - size_after

    final_filename = os.path.splitext(pdf_name)[0] + '.jpg.pdf'
    logging.info('Saved %d bytes to create %s.', total_savings, final_filename)
    my_pdf.save(final_filename)

    my_pdf.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    with tempfile.TemporaryDirectory() as tmpdirname:
        logging.debug('    **** Temporary directory created: %s', tmpdirname)
        os.environ['TMPDIR'] = tmpdirname
        main(tmpdirname, sys.argv[1])
