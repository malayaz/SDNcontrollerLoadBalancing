#!/bin/bash
apt-get update
apt-get -y install unzip
apt-get -y install make
apt-get -y install build-essential
apt-get -y install libpcap0.8-dev
apt-get -y install autoconf
apt-get -y install automake
apt-get -y install libtool
apt-get -y install libnet1-dev
unzip arping-arping-2.14.zip
cd arping-arping-2.14
libtoolize
aclocal
autoconf
autoheader
automake --add-missing
./configure
make
make install
