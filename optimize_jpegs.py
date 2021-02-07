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


# Brute-force determination of the number of (non-inlined) images in the
# file. Ideally, this should be supported by pikepdf, but it currently
# isn't, AFAIK.
def num_image_objects(pdf):
    """
    Return number of external images in the PDF document pdf.
    """
    return sum(1 for obj in pdf.objects if isinstance(obj, pikepdf.Stream)
               and '/Subtype' in obj and obj['/Subtype'] == '/Image')


# Generator to iterate over (non-inlined) image objects more pythonic
def image_objects(pdf):
    """
    Iterates over (non-inlined) image objects in the PDF document pdf.
    """
    for obj in pdf.objects:
        if isinstance(obj, pikepdf.Stream) and '/Subtype' in obj and obj['/Subtype'] == '/Image':
            yield obj


def delete_name(obj, name, num=None):
    """
    Remove a PDF name from object obj with number num.
    """
    if name in obj:
        del obj[name]
        print(f'    **** Removed name: {name} from obj {num}.')


def main(tmpdirname, pdf_name):
    """
    Entry point of the program.
    """
    total_savings = 0

    logging.info('Processing %s.', pdf_name)

    my_pdf = pikepdf.open(pdf_name)

    img_num = 0
    # total_objs = num_image_objects(mypdf)
    # for image_obj in tqdm(image_objects(my_pdf), total=total_objs):
    for image_obj in image_objects(my_pdf):

        if '/Filter' not in image_obj:
            continue

        # FIXME: decode also if a DCT encoded object has a Deflate filter
        # (or other filters like base85, RLE etc).
        # FIXME: to improve *a lot*
        if (image_obj.Filter != '/DCTDecode' and
            not (isinstance(image_obj.Filter, pikepdf.Array) and
                 len(image_obj.Filter) == 1 and
                 image_obj.Filter[0] == '/DCTDecode')):
            continue

        # Unfortunately, jpgcrush only works with RGB or grayscale images.
        if image_obj.ColorSpace == '/DeviceCMYK':
            continue

        img_num += 1
        logging.debug('Found a JPEG as %s', image_obj.ColorSpace)

        tempname = os.path.join(tmpdirname, f'img-{img_num:05d}.jpg')
        source = open(tempname, 'wb')

        size_before = source.write(image_obj.read_raw_bytes())
        logging.debug('Wrote %d bytes to the tempfile %s.', size_before, tempname)
        source.close()

        subprocess.check_call(['jpgcrush', tempname])

        # Use exiftool to remove jpeg metadata. It is carefult to not remove
        # some metadata (in particular Adobe's "APP14" metadata) that
        # interferes with how the image colors are decoded.  See
        # https://exiftool.org/forum/index.php?topic=6448.msg32114#msg32114
        # for information from Exiftool's author.
        subprocess.check_call(['exiftool', '-overwrite_original', '-all=', source.name])

        targetfn = open(tempname, 'rb')
        target = targetfn.read()

        size_after = len(target)
        logging.debug('Read back %d bytes from the tempfile %s.', size_after, tempname)
        image_obj.write(target, filter=pikepdf.Name('/DCTDecode'))
        logging.debug('The image is back on the PDF file.')

        total_savings += size_before - size_after

    final_filename = os.path.splitext(pdf_name)[0] + '.jpg.pdf'
    logging.info('Saved %d bytes to create %s', total_savings, final_filename)

    delete_name(my_pdf.trailer, '/Info', -2)

    my_pdf.remove_unreferenced_resources()
    my_pdf.save(final_filename, fix_metadata_version=False)

    my_pdf.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    for filename in sys.argv[1:]:
        with tempfile.TemporaryDirectory() as tmpdirname:
            logging.debug('    **** Temporary directory created: %s', tmpdirname)
            os.environ['TMPDIR'] = tmpdirname
            main(tmpdirname, filename)
