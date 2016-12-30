#!/bin/bash
a=1
b=1
while [ $a -eq $b ]
do
Timeout=$((4000 + RANDOM % 6000))
arping 192.168.1.45 -q -c 1 -i eth1 -w $Timeout
echo $Timeout
done
