#!/usr/bin/env python3
'''
This program removes some metadata from PDF files and tries to optimize
JPEG files that it may contain. It is meant as a pre-processing step before
running `pdfsizeopt`.

Apart from Python itself, this program depends on the following programs or
modules:

* pikepdf (Debian package: python3-pikepdf)
* exiftool (Debian package: libimage-exiftool-perl)
* A patched version of jpgcrush (to optimize files crossing filesystems)

A patched version of jpgcrush can be obtained from my PPA at:

    https://launchpad.net/~rbrito/+archive/ubuntu/ppa

While you are at it, you probably also want to grab a copy of jbig2enc.
'''

import argparse
import logging
import os.path
import subprocess
import tempfile

import pikepdf

# Here we list what kind of metadata we remove from the PDF.
UNDESIRED_NAMES = [
    # From the infodict
    '/AcroForm',
    '/Author',
    '/Creator',
    '/Keywords',
    '/OpenAction',
    '/Producer',
    '/Subject',
    '/ViewerPreferences',
    '/Lang',
    '/Info',
    '/PageLayout',
    '/PageMode',
    '/Version',

    # FIXME: Optional Content (sometimes, hidden, sometimes not)
    # '/OCProperties',

    # Date stuff
    '/CreationDate',
    '/LastModified',
    '/ModDate',

    # pdftex stuff
    '/PTEX.Fullbanner',
    '/PTEX.FileName',
    '/PTEX.InfoDict',
    '/PTEX.PageNumber',

    # Generic
    '/Metadata',

    # From images
    '/PieceInfo',
    '/ImageName',

    # From pages
    '/Thumb',

    # From other software
    '/ITXT',
    '/Lambkin',

    # Embedded files
    '/EmbeddedFiles',

    # From annotations.
    '/NM',  # FIXME: Test; maybe should not be removed
    # '/RC',  # FIXME: idem

    # FIXME: remove /SWF files (and other names) from a /Navigator entry
    # (adobe extensions level 3).
    '/RichMediaExecute',
    '/ProcSet',  # "Acrobat 5.0 and later ignores procedure sets." (page 126)
]


# Auxiliary functions for removing PDF metadata
def delete_javascript(obj, num):
    if ('/JS' in obj) and ('/S' in obj):
        del obj['/JS']
        del obj['/S']
        logging.info('    **** Removed Javascript from obj %d.', num)


def delete_annotations_moddate(obj, num):
    if ('/Type' in obj) and (obj.Type == '/Annot') and '/M' in obj:
        del obj['/M']
        logging.info('    **** Removed /M from obj %d.', num)


def delete_annotations_rc(obj, num):
    if ('/Subtype' in obj) and (obj.Subtype == '/FreeText') and '/RC' in obj:
        del obj['/RC']
        logging.info('    **** Removed /RC from obj %d.', num)


def delete_annotations_t(obj, num):
    if ('/Subtype' in obj) and (obj.Subtype == '/FreeText') and '/T' in obj:
        del obj['/T']
        logging.info('    **** Removed /T from obj %d.', num)


def delete_annotations_c(obj, num):
    if ('/Subtype' in obj) and (obj.Subtype == '/FreeText') and '/C' in obj:
        del obj['/C']
        logging.info('    **** Removed /C from obj %d.', num)


def delete_name(obj, name, num=None):
    if name in obj:
        del obj[name]
        logging.info('    **** Removed name: %s from obj %d.', name, num)


# Auxiliary functions for optimizing JPEGs
def num_image_objects(pdf):
    """
    Return number of external images in the PDF document pdf.

    This function performs a brute-force determination of the number of
    (non-inlined) images in the pdf file.

    Ideally, this operation should be supported by pikepdf, but it currently
    isn't, AFAIK.
    """
    return sum(1 for obj in pdf.objects if isinstance(obj, pikepdf.Stream)
               and '/Subtype' in obj and obj['/Subtype'] == '/Image')


def image_objects(pdf):
    """
    Iterates over (non-inlined) image objects in the PDF document pdf.

    This provides a generator to iterate over (non-inlined) image objects to
    make the code that calls it more pythonic.
    """
    for obj in pdf.objects:
        if isinstance(obj, pikepdf.Stream) and '/Subtype' in obj and obj['/Subtype'] == '/Image':
            yield obj


def optimize_jpegs(tmpdirname, my_pdf):
    """
    Given a tmpdirname and a PDF object, this function iterates over the
    non-inline images that are DCT encoded (i.e., JPEGs) and tries to
    optimize them, by:

    * optimizing the Huffman tables of the JPEGs
    * removing non-essential metadata from the JPEGs.
    """
    total_savings = 0

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

    return total_savings


def perform_optimizations(tmpdirname, filename, remove_js=False):
    """
    Opens the file and delegates the optimizations.

    The file to operate on is named filename and it will use a temporary
    directory called tmpdirname for whatever it needs.

    tmpdirname will be needed to optimize the JPEG files contained in the
    PDF file, as we will delegate the task to jpgcrush and to exiftool.
    """
    logging.info('Processing %s', filename)
    original_size = os.path.getsize(filename)
    my_pdf = pikepdf.open(filename)

    # Here we actually process the file
    delete_metadata(my_pdf, remove_js)
    savings_with_images = optimize_jpegs(tmpdirname, my_pdf)

    my_pdf.remove_unreferenced_resources()
    final_filename = os.path.splitext(filename)[0] + '.clean.pdf'
    my_pdf.save(final_filename, fix_metadata_version=False)

    final_size = os.path.getsize(final_filename)
    total_savings = original_size - final_size

    logging.info('Saved %d bytes (%d in images) to create %s',
                 total_savings, savings_with_images, final_filename)


def delete_metadata(my_pdf, remove_js):
    num_of_objects = my_pdf.trailer['/Size']  # this includes the object 0

    # FIXME: somehow, using enumerate seems slower, when profiling with a
    # large file:
    #
    # perf stat --repeat=10 using_pikepdf.py \
    # katz-lindell-introduction-to-modern-cryptography.pso.pdfa.unc.pso.pso.pdf

    # Traverse all the objects
    # for i, cur_obj in enumerate(my_pdf.objects):
    for i in range(1, num_of_objects):

        cur_obj = my_pdf.get_object(i, 0)

        # Stuff that doesn't contain keys
        if isinstance(cur_obj, (pikepdf.String, pikepdf.Array, pikepdf.Name)):
            continue
        if not isinstance(cur_obj, (pikepdf.objects.Object, pikepdf.Stream)):
            continue

        for name in UNDESIRED_NAMES:
            delete_name(cur_obj, name, i)

        if remove_js:
            delete_javascript(cur_obj, i)
        delete_annotations_moddate(cur_obj, i)

        # Not working right now
        # delete_annotations_rc(cur_obj, i)
        # delete_annotations_t(cur_obj, i)
        delete_annotations_c(cur_obj, i)

    # Remove from the document root
    for name in UNDESIRED_NAMES:
        delete_name(my_pdf.Root, name)

    # FIXME: The following may be useless with the deletions above
    # Remove the only /Title that we want
    delete_name(my_pdf.docinfo, '/Title', -1)
    delete_name(my_pdf.docinfo, '/OpenAction', -1)

    # Remove any other stuff from the docinfo dictionary
    for key in my_pdf.docinfo.keys():
        delete_name(my_pdf.docinfo, key, -1)

    # FIXME: This doesn't seem to work
    delete_name(my_pdf.Root, '/Info')
    # FIXME: This does
    delete_name(my_pdf.trailer, '/Info', -2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove metadata from PDF and try to optimize their JPGs.')

    parser.add_argument('--remove-js', action='store_true', default=False,
                        help='remove JavaScript from PDFs. (Default: False)')
    parser.add_argument('filename', nargs='+',
                        help='name of the file(s) to process')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    for filename in args.filename:
        with tempfile.TemporaryDirectory() as tmpdirname:
            logging.debug('    **** Temporary directory created: %s', tmpdirname)
            # FIXME: Document why we have to set TMPDIR
            os.environ['TMPDIR'] = tmpdirname
            perform_optimizations(tmpdirname, filename, args.remove_js)
