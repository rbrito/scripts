#!/bin/bash

set -e

OPTIMIZER=~/Downloads/pdfsizeopt/pdfsizeopt

case $1 in
    --help)
        echo "$0 --optimize-{ultrafast,fast,normal,extra,ultra} <input.pdf>"
        exit 0
        ;;
    --optimize-ultrafast)
        IMAGE_OPTIMIZERS=jbig2
        shift
        ;;
    --optimize-fast)
        IMAGE_OPTIMIZERS=rbrito0,jbig2
        shift
        ;;
    --optimize-normal)
        IMAGE_OPTIMIZERS=rbrito,jbig2
        shift
        ;;
    --optimize-extra)
        IMAGE_OPTIMIZERS=pngout,rbrito3,jbig2
        shift
        ;;
    --optimize-ultra)
        IMAGE_OPTIMIZERS=zopflipng,pngout3,rbrito3,jbig2
        shift
        ;;
    *)
        IMAGE_OPTIMIZERS=rbrito,jbig2
esac


qpdf --stream-data=uncompress --compress-streams=n --decode-level=specialized "$1" "${1%%pdf}unc.pdf"

$OPTIMIZER --use-image-optimizer=$IMAGE_OPTIMIZERS --do-fast-bilevel-images=yes --use-multivalent=no "${1%%pdf}unc.pdf"
$OPTIMIZER --use-image-optimizer=$IMAGE_OPTIMIZERS --do-fast-bilevel-images=yes --use-multivalent=yes --do-optimize-images=no "${1%%pdf}unc.pso.pdf"
$OPTIMIZER --use-image-optimizer=$IMAGE_OPTIMIZERS --do-fast-bilevel-images=yes --use-multivalent=no --do-optimize-images=no "${1%%pdf}unc.pso.psom.pdf"

$OPTIMIZER --use-image-optimizer=$IMAGE_OPTIMIZERS --do-fast-bilevel-images=yes --use-multivalent=no "${1%%pdf}pdf"
$OPTIMIZER --use-image-optimizer=$IMAGE_OPTIMIZERS --do-fast-bilevel-images=yes --use-multivalent=yes --do-optimize-images=no "${1%%pdf}pso.pdf"
$OPTIMIZER --use-image-optimizer=$IMAGE_OPTIMIZERS --do-fast-bilevel-images=yes --use-multivalent=no --do-optimize-images=no "${1%%pdf}pso.psom.pdf"
