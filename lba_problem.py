#!/usr/bin/env python

def problematic_block(lba, first_part_sec, sec_size, blk_size):
    """Given the number (LBA) of a problematic sector on a disk, the number of
    the first sector of the partition that contains the LBA, the sector size
    of the disk and the block size of the filesystem, return the number of
    the filesystem block that contains the problematic sector.

    The number of the sector is usually found in a dmesg log or on the
    output of SMART checking tools, like `skdump` or `smartctl`.

    Example for a regular ext4 filesystem on a disk with 512-byte sectors:
    
    >>> problematic_block(1453654754, 499712, 512, 4096)
    181644380
    >>>
    """

    return (lba - first_part_sec) * sec_size // blk_size

    # /home/rbrito/videos/Lectures/coursera/videos/COMPLETED/comnetworks-002/05_Week_5-_Routing/09_5-9_Hierarchical_Routing.mp4
    # dd if=/dev/zero of=/dev/sda2 bs=4096 count=1 seek=181644380
