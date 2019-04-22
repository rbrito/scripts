#!/bin/sh

set -e

# Note: mktemp instead of the other insecure alternatives
WORKDIR="$(mktemp -d)"
CURDIR="$PWD"
REALPATH="$(realpath "$1")"
ORIGDIR="$(dirname "$REALPATH")"
ORIGNAME="$(basename "$REALPATH")"
NEWNAME="$ORIGDIR/${ORIGNAME%%pdf}repack.pdf"

cd "$WORKDIR"

pdfimages -j -tiff "$REALPATH" a
jhead -purejpg *.jpg
jpgcrush *.jpg
pingo -lossless -s9 -verbose=3 *.png

# exiftool -Xresolution=600 -Yresolution=600 -ResolutionUnit=inches *.tif

img2pdf --verbose -o "$NEWNAME" *

cd "$CURDIR"
rm -rf "$WORKDIR"
