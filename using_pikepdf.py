#!/usr/bin/env python3

import os.path
import sys

import pikepdf


UNDESIRED_NAMES = [
    # From the infodict
    '/AcroForm',
    '/Author',
    '/CreationDate',
    '/Creator',
    '/Keywords',
    '/OpenAction',
    '/Producer',
    '/Subject',
    '/ViewerPreferences',

    # '/OCProperties',  # Optional Content (sometimes, hidden, sometimes not)

    # Date stuff
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
]


def delete_javascript(obj, num):
    if ('/JS' in obj) and ('/S' in obj):
        del obj['/JS']
        del obj['/S']

        print('    **** Removed Javascript from obj %d.' % num)


def delete_name(obj, name, num=None):
    # if num is not None:
    #     print('    **** Object %s, Name: %s, objnum: %d.' % (type(obj), name, num))

        if name in obj:
            del obj[name]
            print('    **** Removed name: %s from obj %d.' % (name, num))


if __name__ == '__main__':
    my_pdf = pikepdf.open(sys.argv[1])

    num_of_objects = my_pdf.trailer['/Size']  # this includes the object 0

    # FIXME: somehow, using enumerate seems slower, when profiling with a large file:
    #
    # perf stat --repeat=10 using_pikepdf.py \
    # katz-lindell-introduction-to-modern-cryptography.pso.pdfa.unc.pso.pso.pdf

    # Traverse all the objects
    for i in range(1, num_of_objects):
    # for i, cur_obj in enumerate(my_pdf.objects):

        cur_obj = my_pdf.get_object(i, 0)

        # Stuff that doesn't contain keys
        if isinstance(cur_obj, (pikepdf.String, pikepdf.Array, pikepdf.Name)):
            continue
        if not isinstance(cur_obj,
                          (pikepdf.objects.Object, pikepdf.Stream)):
            continue

        for name in UNDESIRED_NAMES:
            delete_name(cur_obj, name, i)

        delete_javascript(cur_obj, i)

    # Remove from the document
    for name in UNDESIRED_NAMES:
        delete_name(my_pdf.root, name)

    # FIXME: This doesn't seem to work
    delete_name(my_pdf.root, '/Info')

    # FIXME: This does
    delete_name(my_pdf.trailer, '/Info', -2)

    ## FIXME: The following may be useless with the deletion above

    # Remove the only /Title that we want
    delete_name(my_pdf.docinfo, '/Title', -1)
    delete_name(my_pdf.docinfo, '/OpenAction', -1)

    # Remove any other stuff from the docinfo dictionary
    for key in my_pdf.docinfo.keys():
        delete_name(my_pdf.docinfo, key, -1)

    # FIXME: Perhaps use pdfsizeopt instead?
    # my_pdf.remove_unreferenced_resources()
    my_pdf.save(os.path.splitext(sys.argv[1])[0] + '.clean.pdf')
