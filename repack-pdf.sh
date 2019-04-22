#!/bin/sh

#set -e

KEEP_TEMP_DIR=0

case $1 in
    --help)
        echo "$0 [--keep-temp-dir] <input.pdf>"
        exit 0
        ;;
    --keep-temp-dir)
        KEEP_TEMP_DIR=1
        shift
        ;;
esac


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

if [ $KEEP_TEMP_DIR = 0 ]; then
    rm -rf "$WORKDIR"
fi
