#!/usr/bin/env python

"""Small program to assist with the automation of the steps listed in the
[Bad Blocks HOWTO][1] for reallocating damaged sectors of a hard drive
(after some unfortunate events).

[1]: http://smartmontools.sourceforge.net/badblockhowto.html

Unfortunately, the method that I have so far is to use a pipe with programs
from the e2fsprogs package and parse its output, which is admittedly not a
robust solution to the problem.

Given the number (LBA) of a problematic sector on a disk, the number of
the first sector of the partition that contains the LBA, the sector size
of the disk and the block size of the filesystem, we try to determine if
there is any file that may be damaged, and, if there is, then what they are.

The number of the sector is usually found in a dmesg log or on the
output of SMART checking tools, like `skdump` or `smartctl`.

You can, after such an unfortunate event, decide what to do (Copy whatever
is left of the file with problems? Redownload it? Recover from backups?)
and, then, issue a write command specifically to that sector, so that you
can force a reallocation of the sector to some spare sectors that the drive
may have (hopefully, it has some) with:

    dd if=/dev/zero of=/dev/sda2 bs=4096 count=1 seek=<B>

where B is the block number returned by the function `problematic_block`.
Of course, adjust /dev/sda2 to the appropriate (raw) block device and the
block site (bs parameter to dd) with the block size of your filesystem.

The detection of the names of filesystems only work with ext2/3/4
filesystems (since we depend on debugfs to find the names of the potentially
damaged files).
"""

import re
from subprocess import (call, PIPE)


def problematic_block(lba, first_part_sec, sec_size=512, blk_size=4096):
    """Given the number (LBA) of a problematic sector on a disk, the number of
    the first sector of the partition that contains the LBA, the sector size
    of the disk and the block size of the filesystem, return the number of
    the filesystem block that contains the problematic sector.

    first_part_sec is usually obtained from the output of `fdisk -l` on the
    problematic drive.

    The number of the sector (the lba argument to this function) is usually
    found in a dmesg log or on the output of SMART checking tools, like
    `skdump` or `smartctl`.

    Example for a regular ext4 filesystem on a disk with 512-byte sectors:

    >>> problematic_block(1453654754, 499712, 512, 4096)
    181644380
    >>>
    """

    return (lba - first_part_sec) * sec_size // blk_size


def debugfs_discover_filename(blocknum, devnode):
    """Given a block number blocknum of an ext2/3/4 filesystem specified by
    devnode, try to find the name of the file in that filesystem that
    contains that block, if any.

    We assume that blocknum is a valid block number for the device devnode.

    We return None if the block is not associated with any file or return a
    list of strings containing the full path (absolute) for files that
    contain such block. Exception: the journal of the filesystem is
    represented as an empty string.

    One (unfortunate) use case of this function is to discover which files
    in an ext2/3/4 filesystem are affected by the problematic block given by
    blocknum.
    """
    p1 = call(['debugfs',
               '-R',
               'testb',
               str(blocknum),
               devnode], stdout=PIPE)
    stdout, _ = p1.communicate()
    p1.stdout.close()
    lines = stdout.split('\n')

    if len(lines) != 1:  # this is not really expected
        raise Exception('Foo barred.')

    mobj = re.search('not in use$', lines[0])
    if mobj is None:  # fortunate case: not in use
        return None

    p1 = call(['debugfs',
               '-R',
               'icheck',
               str(blocknum),
               devnode], stdout=PIPE)
    stdout, _ = p1.communicate()
    p1.stdout.close()
    lines = stdout.split('\n')

    if len(lines) != 2:  # this is not really expected
        raise Exception('Foo barred.')

    mobj = re.search(r'\s+(\d+)$', lines[1])
    if mobj is None:
        raise Exception('Foo barred.')

    p1 = call(['debugfs',
               '-R',
               'ncheck',
               mobj.group(1),  # there may be multiple inodes?
               devnode], stdout=PIPE)
    stdout, _ = p1.communicate()
    p1.stdout.close()
    lines = stdout.split('\n')

    result = []
    for line in lines[1:]:
        mobj = re.search(r'^\d+\t(.*)?', line)
        if mobj is not None:
            result.append(mobj.group(1))

    return result

    # /home/rbrito/videos/Lectures/coursera/videos/COMPLETED/comnetworks-002/05_Week_5-_Routing/09_5-9_Hierarchical_Routing.mp4
    # dd if=/dev/zero of=/dev/sda2 bs=4096 count=1 seek=181644380
