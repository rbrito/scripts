#!/bin/sh

mkdir temp
cd temp

pdfimages -tiff ../"$1" a
jhead -purejpg *.jpg
jpgcrush *.jpg
pingo -lossless -s9 -verbose=3 *.png


img2pdf --verbose -o ../"${1%%pdf}repack.pdf" *

#cd ..
#rm -rf temp
