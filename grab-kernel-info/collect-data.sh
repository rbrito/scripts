#!/bin/sh

DATE=$(date +%s)
KVER=$(uname -r)
MACH=$(uname -n)
DIR=$MACH-$DATE-linux-$KVER
mkdir $DIR
cd $DIR

cp /boot/config-$KVER		.
cp /proc/cpuinfo		proc-cpuinfo.txt
cp /proc/interrupts		proc-interrupts.txt
cp /proc/iomem			proc-iomem.txt
cp /proc/ioports		proc-ioports.txt
cp /var/log/Xorg.0.log		.

uname -a			> uname-a.txt
dmesg -s $((128 * 1024))	> $DATE-dmesg-$KVER.log
acpidump			> acpidump.txt
dmidecode			> dmidecode.txt

lspci -v			> lspci-v.txt
lspci -vvxx			> lspci-vvxx.txt
lspci -vx			> lspci-vx.txt
lspci				> lspci.txt
lsusb				> lsusb.txt
lsmod				> lsmod.txt

lshw				> lshw.txt

mount -t debugfs none /sys/kernel/debug/
tar cf debugfs-$DATE.tar /sys/kernel/debug

cd ..
tar jcf $DIR.tar.bz2 $DIR
