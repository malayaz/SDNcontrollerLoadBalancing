#!/bin/bash

while :
do
ovs-vsctl list controller | grep -e is_connected -e target -e role > role.txt
cat role.txt
printf "\033[F"
printf "\033[F"
printf "\033[F"
printf "\033[F"
printf "\033[F"
printf "\033[F"
printf "\033[F"
printf "\033[F"
printf "\033[F"

done


