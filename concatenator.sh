#!/bin/sh

#mkdir mkv
#mv *.mkv mkv

EXT=flv

mediainfo --Inform='General;%Duration/String3%\n%FileName%\n' *.$EXT | ~/src/utils/simplechaps.py > chaps.txt

mkvmerge --chapters chaps.txt \
    -o ../$(basename $(pwd)).mkv \
    01-* \
    $(for i in $(seq -w 2 $(ls -1 *.$EXT | wc -l)); do echo + $i*; done)
