#!/bin/sh

# dependencies: optipng, advancecomp, symlinks, rdfind, parallel, python-scour

find . -iname "*.png" -type f -print0 | xargs -0 optipng -zc1-9 -zm1-9 -zs0-3 -f0-5
find . -iname "*.png" -type f -print0 | xargs -0 advpng -z3
find . -iname "*.png" -type f -print0 | xargs -0 advpng -z4
find . -iname "*.png" -type f -print0 | xargs -0 advdef -z3
find . -iname "*.png" -type f -print0 | xargs -0 advdef -z4
find . -iname "*.png" -type f -print0 | xargs -0 advdef -z4 -i 20


symlinks -r -c -v -s .

rdfind -makesymlinks true .

find . -iname "*.svg" -type f -print0 | parallel -0 'scour -o {}.opt -i {} --create-groups --enable-id-stripping --enable-comment-stripping --shorten-ids --remove-metadata && mv {}.opt {}'
