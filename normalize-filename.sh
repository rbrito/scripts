#!/bin/sh

# First, some noisy symbols
# Second, some redundant extensions
# Third, substituting runs of characters
# Fourth, making everything lowercase

prename -e "s/'//g; s/ +/-/g; s/,/-/g; s/_+/_/g; s/-+/-/g; s/\[//g; s/\]//g; s/\(//g; s/\)//g; s/\{//g; s/\}//g; s/&//g; s/ /-/g; s/_/-/g; s/\.-/-/g; s/-\././g; s/-\././g; s/;/-/g; s/-o\.pdf$/.pdf/g; s/-o\.pdf\././g; s/\.unc\././g; s/\.qpdf\././g; s/\.opt\././g; s/\.03-metadata-removed\././g; s/\.decrypted\././g; s/\.linear\././g; s/\.ocr\././g; s/\.new\.pdf\.repack\././g; s/\.pso\.pdf\.repack\././g; s/\.pso\.pso\./.pso./g; s/\.pso\.psom\./.psom./g; s/\.psom\.psom\./.psom./g; s/\.pdf\.pso\./.pso./g; s/\.pdf\.psom\./.psom./g; s/\.\.+/./g; s/-+/-/g; y/A-Z/a-z/;" *
