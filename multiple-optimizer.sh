#!/bin/bash

OPTIMIZER=~/Downloads/pdfsizeopt/pdfsizeopt

qpdf --stream-data=uncompress --compress-streams=n --decode-level=specialized "$1" "${1%%pdf}unc.pdf"


$OPTIMIZER --use-image-optimizer=rbrito,jbig2 --use-multivalent=no "${1%%pdf}unc.pdf"
$OPTIMIZER --use-image-optimizer=rbrito,jbig2 --use-multivalent=yes --do-optimize-images=no "${1%%pdf}unc.pso.pdf"
$OPTIMIZER --use-image-optimizer=rbrito,jbig2 --use-multivalent=no --do-optimize-images=no "${1%%pdf}unc.pso.psom.pdf"

$OPTIMIZER --use-image-optimizer=rbrito,jbig2 --use-multivalent=no "${1%%pdf}pdf"
$OPTIMIZER --use-image-optimizer=rbrito,jbig2 --use-multivalent=yes --do-optimize-images=no "${1%%pdf}pso.pdf"
$OPTIMIZER --use-image-optimizer=rbrito,jbig2 --use-multivalent=no --do-optimize-images=no "${1%%pdf}pso.psom.pdf"
