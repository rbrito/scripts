#!/bin/sh

DATE=$(date +%s)
KVER=$(uname -r)
DIR=kernel-debug-$DATE
mkdir $DIR
cd $DIR

cp /boot/config-$KVER		.
cp /proc/cpuinfo		proc-cpuinfo.txt
cp /proc/interrupts		proc-interrupts.txt
cp /proc/iomem			proc-iomem.txt
cp /proc/ioports		proc-ioports.txt
cp /var/log/Xorg.0.log		.

uname -a			> uname-a.txt
dmesg				> $DATE-dmesg-$KVER.log
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
tar cvf debugfs-$DATE.tar /sys/kernel/debug

cd ..
tar jcvf $DIR.tar.bz2 $DIR
