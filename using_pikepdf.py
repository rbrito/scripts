#!/usr/bin/env python3

import os.path
import sys

import pikepdf


undesired_names = [
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


def delete_name(obj, name, num=None):
    # if num is not None:
    #     print('    **** Object %s, Name: %s, objnum: %d.' % (type(obj), name, num))

        if name in obj:
            del obj[name]
            print('    **** Removed name: %s from obj %d.' % (name, num))


if __name__ == '__main__':
    my_pdf = pikepdf.open(sys.argv[1])

    num_of_objects = my_pdf.trailer['/Size']  # this includes the object 0

    # Traverse all the objects
    for i in range(1, num_of_objects):
        cur_obj = my_pdf.get_object(i, 0)

        # Stuff that doesn't contain keys
        if isinstance(cur_obj, (pikepdf.String, pikepdf.Array, pikepdf.Name)):
            continue
        if not isinstance(cur_obj,
                          (pikepdf.objects.Object, pikepdf.Stream)):
            continue

        for name in undesired_names:
            delete_name(cur_obj, name, i)

    # Remove from the document
    for name in undesired_names:
        delete_name(my_pdf.root, name)

    # FIXME: This doesn't seem to work
    delete_name(my_pdf.root, '/Info')

    # FIXME: Perhaps use pdfsizeopt instead?
    my_pdf.remove_unreferenced_resources()
    my_pdf.save(os.path.splitext(sys.argv[1])[0] + '.clean.pdf')
