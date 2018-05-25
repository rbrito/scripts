#!/bin/sh

borg create \
     --verbose \
     --stats \
     --compression zlib \
     --progress \
     --one-file-system \
     --exclude-caches \
     --exclude-from /root/borg-dont-backup.txt \
     /media/rbrito/Seagate-2000GB-1/borg-backups/::'{hostname}-{utcnow}' \
     /

