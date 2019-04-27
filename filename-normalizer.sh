#!/bin/sh

prename -e "s/'//g; s/\.03-metadata-removed\././g; s/\.linear\././g; s/\.unc\././g; s/\.new\.pdf\.repack\././g; s/\.pso\.pdf\.repack\././g; s/\.pso\.pso\./.pso./g; s/\.psom\.psom\./.psom./g; s/\.pso\.psom\./.psom./; s/-o\.pdf\././g; s/ +/-/g; s/,/-/g; s/_+/_/g; s/-+/-/g; s/\[//g; s/\]//g; s/\)//g; s/\(//g; s/\{//g; s/\}//g; s/&//g; s/ /-/g; s/_/-/g; s/\.-/-/g; s/-\././g; s/-\././g; s/'//g; s/;/-/g; s/\.pdf\.pso\./.pso./g; s/\.pdf\.psom\./.psom./g; s/\.\.+/./g; s/-+/-/g; y/A-Z/a-z/;" *
