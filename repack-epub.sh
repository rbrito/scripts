#!/bin/sh

# FIXME: Quote everything for whitespace!

# Note: mktemp instead of the other insecure alternatives
WORKDIR=$(mktemp -d)

cd $WORKDIR
unzip $1

# TODO: Sanity check: verify if we're at the top level of the epub

# Fix permissions
find . -type d -print0 | xargs -0 chmod 755
find . -type f -print0 | xargs -0 chmod 644

# Optimize PNGs
find . -iname "*.png" -print0 | xargs -0 optipng -o4
find . -iname "*.png" -print0 | xargs -0 advpng -z3
find . -iname "*.png" -print0 | xargs -0 advpng -z4
find . -iname "*.png" -print0 | xargs -0 advdef -z3
find . -iname "*.png" -print0 | xargs -0 advdef -z4

# Optimize JPGs
find . -iname "*.jpg" -o -iname "*.jpeg" -print0 | xargs -0 jpgcrush
find . -iname "*.jpg" -o -iname "*.jpeg" -print0 | xargs -0 jhead -purejpg

