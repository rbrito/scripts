#!/usr/bin/env python3

import logging
import os.path
import subprocess
import sys
import tempfile

import pikepdf

# FIXME: Use the progress bar when we suppress the output of forked
# commands.
#
# Forking is, of course, very expensive and, at least, jpgcrush uses a Perl
# process that interprets code that also forks processes, making everything
# very expensive.
#
# FIXME: To use a progress bar with tqdm and avoid output from being messed
# up, we can steal code from ocrmypdf, since it has a wrapper around tqdm
# that allows output generation and not losing the bar.
#


# from tqdm import tqdm

# # Stolen from ocrmypdf
# class TqdmConsole:
#     """Wrapper to log messages in a way that is compatible with tqdm progress bar"""

#     def __init__(self, file):
#         self.file = file
#         self.py36 = sys.version_info[0:2] == (3, 6)

#     def write(self, msg):
#         # When no progress bar is active, tqdm.write() routes to print()
#         if self.py36:
#             if msg.strip() != '':
#                 tqdm.write(msg.rstrip(), end='\n', file=self.file)
#         else:
#             tqdm.write(msg.rstrip(), end='\n', file=self.file)

#     def flush(self):
#         if hasattr(self.file, "flush"):
#             self.file.flush()


# Brute-force determination of the number of (non-inlined) images in the
# file. Ideally, this should be supported by pikepdf, but it currently
# isn't, AFAIK.
def num_image_objects(pdf):
    return sum(1 for obj in pdf.objects if isinstance(obj, pikepdf.Stream)
               and '/Subtype' in obj and obj['/Subtype'] == '/Image')


# Generator to make the following code more pythonic
def image_objects(pdf):
    for obj in pdf.objects:
        if isinstance(obj, pikepdf.Stream) and '/Subtype' in obj and obj['/Subtype'] == '/Image':
            yield obj


def main(tmpdirname, pdf_name):
    total_savings = 0

    logging.info('Processing %s.', pdf_name)

    my_pdf = pikepdf.open(pdf_name)

    # total_objs = num_image_objects(mypdf)
    # for image_obj in tqdm(image_objects(my_pdf), total=total_objs):
    for image_obj in image_objects(my_pdf):

        if '/Filter' not in image_obj:
            continue

        # FIXME: to improve *a lot*
        if (image_obj.Filter != '/DCTDecode' and
           not (isinstance(image_obj.Filter, pikepdf.Array) and
                len(image_obj.Filter) == 1 and
                image_obj.Filter[0] == '/DCTDecode')):
            continue

        if not (image_obj.ColorSpace in ('/DeviceRGB', '/DeviceGray') or
                (isinstance(image_obj.ColorSpace, pikepdf.Array) and
                 image_obj.ColorSpace[0] == '/DeviceN' and image_obj.ColorSpace[2] in
                 ('/DeviceRGB', '/DeviceGray'))):
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

        # Unfortunately, the -purejpg of jhead is too aggressive and may
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

    for filename in sys.argv[1:]:
        with tempfile.TemporaryDirectory() as tmpdirname:
            logging.debug('    **** Temporary directory created: %s', tmpdirname)
            os.environ['TMPDIR'] = tmpdirname
            main(tmpdirname, filename)
