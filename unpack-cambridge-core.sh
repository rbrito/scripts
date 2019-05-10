#!/bin/sh

mkdir done old

unzip "$1"
PDFFILE="${1%%zip}pdf"
qpdf --empty --pages *.pdf -- "$PDFFILE"
~/Downloads/pdfsizeopt/pdfsizeopt --use-image-optimizer=pingo9,rbrito,jbig2 --use-multivalent=no --do-optimize-images=yes --do-fast-bilevel-images=yes "$PDFFILE"
diffpdf "$PDFFILE" "${PDFFILE%%pdf}pso.pdf"

mv "${PDFFILE%%pdf}pso.pdf" done

rm *.pdf
mv "$1" old
