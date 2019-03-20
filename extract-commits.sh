#!/bin/sh

j=1

for i in $(tac commits.txt); do
    git format-patch --start-number=$j -1 $i
    j=$((j+1))
done
