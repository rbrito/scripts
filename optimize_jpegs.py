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
    return sum(1 for obj in pdf.objects if isinstance(obj, pikepdf.Stream)
               and '/Subtype' in obj and obj['/Subtype'] == '/Image')


# Generator to iterate over (non-inlined) image objects more pythonic
def image_objects(pdf):
    for obj in pdf.objects:
        if isinstance(obj, pikepdf.Stream) and '/Subtype' in obj and obj['/Subtype'] == '/Image':
            yield obj


def singleton_dct_in_array(image_obj):
    imgfilter = image_obj.Filter

    return (isinstance(imgfilter, pikepdf.Array) and
            len(imgfilter) == 1 and
            imgfilter[0] == '/DCTDecode')


def vanilla_colorspaces(image_obj):
    return image_obj.ColorSpace in ('/DeviceRGB', '/DeviceGray')


def devn_colorspaces(image_obj):
    colorspace = image_obj.ColorSpace

    return (isinstance(colorspace, pikepdf.Array) and
            colorspace[0] == '/DeviceN' and
            (colorspace[2] in ('/DeviceRGB', '/DeviceGray')))


def icc_colorspaces(image_obj):
    colorspace = image_obj.ColorSpace

    return (isinstance(colorspace, pikepdf.Array) and
            colorspace[0] == '/ICCBased' and
            (len(colorspace) >= 2 and (('/Alternate' not in colorspace[1]) or
                                       (str(colorspace[1].Alternate) in ('/DeviceRGB', '/DeviceGray')))))


def main(tmpdirname, pdf_name):
    total_savings = 0

    logging.info('Processing %s.', pdf_name)

    my_pdf = pikepdf.open(pdf_name)

    img_num = 0
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

        # Unfortunately, jpgcrush only works with RGB or grayscale images.
        if image_obj.ColorSpace == '/DeviceCMYK':
            continue

        # if not (image_obj.ColorSpace in ('/DeviceRGB', '/DeviceGray') or
        #         (isinstance(image_obj.ColorSpace, pikepdf.Array) and
        #          image_obj.ColorSpace[0] == '/DeviceN' and image_obj.ColorSpace[2] in
        #          ('/DeviceRGB', '/DeviceGray'))):
        #     continue

        # FIXME: Enable this code to process more images
        # if not (image_obj.ColorSpace in ('/DeviceRGB', '/DeviceGray') or
        #         (isinstance(image_obj.ColorSpace, pikepdf.Array) and
        #          image_obj.ColorSpace[0] == '/ICCBased' and str(image_obj.ColorSpace[1].Alternate) in
        #          ('/DeviceRGB', '/DeviceGray'))):
        #     continue

        img_num += 1
        logging.debug('Found a JPEG as %s', image_obj.ColorSpace)

        tempname = os.path.join(tmpdirname, f'img-{img_num:05d}.jpg')
        source = open(tempname, 'wb')

        size_before = source.write(image_obj.read_raw_bytes())
        logging.debug('Wrote %d bytes to the tempfile %s.', size_before, tempname)
        source.close()

        subprocess.check_call(['jpgcrush', tempname])

        # Unfortunately, the -purejpg of jhead is too aggressive and may
        # strip way too much to the point of modifying the image, in some
        # cases.
        subprocess.check_call(['jhead', '-dt', '-dc', '-de', source.name])

        targetfn = open(tempname, 'rb')
        target = targetfn.read()

        size_after = len(target)
        logging.debug('Read back %d bytes from the tempfile %s.', size_after, tempname)
        image_obj.write(target, filter=pikepdf.Name('/DCTDecode'))
        logging.debug('The image is back on the PDF file.')

        total_savings += size_before - size_after

    final_filename = os.path.splitext(pdf_name)[0] + '.jpg.pdf'
    logging.info('Saved %d bytes to create %s', total_savings, final_filename)
    my_pdf.save(final_filename)

    my_pdf.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    for filename in sys.argv[1:]:
        with tempfile.TemporaryDirectory() as tmpdirname:
            logging.debug('    **** Temporary directory created: %s', tmpdirname)
            os.environ['TMPDIR'] = tmpdirname
            main(tmpdirname, filename)
