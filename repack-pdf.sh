#!/bin/sh

mkdir temp
cd temp

pdfimages -all ../"$1" a
jhead -purejpg *.jpg
jpgcrush *.jpg
pingo -lossless -s9 -verbose=3 *.png


img2pdf --verbose --pagesize A4 -o ../"${1%%pdf}repack.pdf" *

cd ..
rm -rf temp
