#!/bin/sh

#set -e

KEEP_TEMP_DIR=0
USE_LOCAL_DIR=0

case $1 in
    --help)
        echo "$0 [--keep-temp-dir] [--use-local-dir] <input.pdf>"
        exit 0
        ;;
    --keep-temp-dir)
        KEEP_TEMP_DIR=1
        shift
        ;;
    --use-local-dir)
        USE_LOCAL_DIR=1
        shift
        ;;
esac


# Note: mktemp instead of the other insecure alternatives
if [ $USE_LOCAL_DIR = 1 ]; then
    WORKDIR="$(mktemp -d --tmpdir=.)"
else
    WORKDIR="$(mktemp -d)"
fi

CURDIR="$PWD"
REALPATH="$(realpath "$1")"
ORIGDIR="$(dirname "$REALPATH")"
ORIGNAME="$(basename "$REALPATH")"
NEWNAME="$ORIGDIR/${ORIGNAME%%pdf}repack.pdf"

cd "$WORKDIR"

pdfimages -j -tiff "$REALPATH" a
find . -iname "*.jpg" -print0 | xargs -0 -r jhead -purejpg
find . -iname "*.jpg" -print0 | xargs -0 -r jpgcrush
find . -iname "*.png" -print0 | xargs -0 -r pingo -lossless -s9 -verbose=3

# exiftool -Xresolution=600 -Yresolution=600 -ResolutionUnit=inches *.tif

# FIXME: extract the pagesize from the original with pdfinfo
# img2pdf --verbose -o "$NEWNAME" --pagesize 421ptx720pt *
img2pdf --verbose -o "$NEWNAME" *

cd "$CURDIR"

if [ $KEEP_TEMP_DIR = 0 ]; then
    rm -rf "$WORKDIR"
fi
