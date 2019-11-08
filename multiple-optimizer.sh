#!/bin/bash

#set -e

OPTIMIZER=~/Downloads/pdfsizeopt/pdfsizeopt

case $1 in
    --help)
        echo -e "$0 -{1,2,3,4,5} <input.pdf>\nLevel 3 is the default."
        exit 0
        ;;
    -1)
        IMAGE_OPTIMIZERS=jbig2
        shift
        ;;
    -2)
        IMAGE_OPTIMIZERS=rbrito0,jbig2
        shift
        ;;
    -3)
        IMAGE_OPTIMIZERS=pingo9,rbrito,jbig2
        shift
        ;;
    -4)
        IMAGE_OPTIMIZERS=pingo9,pngout,rbrito3,jbig2
        shift
        ;;
    -5)
        IMAGE_OPTIMIZERS=pingo9+extra,zopflipng,pngout3,rbrito3,jbig2
        shift
        ;;
    *)
        IMAGE_OPTIMIZERS=pingo9,rbrito,jbig2
esac


qpdf --stream-data=uncompress --compress-streams=n --decode-level=specialized "$1" "${1%%pdf}unc.pdf"

$OPTIMIZER --use-image-optimizer=$IMAGE_OPTIMIZERS --do-fast-bilevel-images=yes --use-multivalent=no "${1%%pdf}unc.pdf"
$OPTIMIZER --use-image-optimizer=$IMAGE_OPTIMIZERS --do-fast-bilevel-images=yes --use-multivalent=yes --do-optimize-images=no "${1%%pdf}unc.pso.pdf"
$OPTIMIZER --use-image-optimizer=$IMAGE_OPTIMIZERS --do-fast-bilevel-images=yes --use-multivalent=no --do-optimize-images=no "${1%%pdf}unc.pso.psom.pdf"

$OPTIMIZER --use-image-optimizer=$IMAGE_OPTIMIZERS --do-fast-bilevel-images=yes --use-multivalent=no "${1%%pdf}pdf"
$OPTIMIZER --use-image-optimizer=$IMAGE_OPTIMIZERS --do-fast-bilevel-images=yes --use-multivalent=yes --do-optimize-images=no "${1%%pdf}pso.pdf"
$OPTIMIZER --use-image-optimizer=$IMAGE_OPTIMIZERS --do-fast-bilevel-images=yes --use-multivalent=no --do-optimize-images=no "${1%%pdf}pso.psom.pdf"
