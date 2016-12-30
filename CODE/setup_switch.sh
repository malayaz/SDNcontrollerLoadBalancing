#!/bin/bash
yum -y install wget gcc make python-devel openssl-devel kernel-devel graphviz kernel-debug-devel autoconf automake rpm-build redhat-rpm-config libtool
mkdir -p ~/rpmbuild/SOURCES
wget http://openvswitch.org/releases/openvswitch-2.3.2.tar.gz
cp openvswitch-2.3.2.tar.gz ~/rpmbuild/SOURCES/
tar xfz openvswitch-2.3.2.tar.gz
sed 's/openvswitch-kmod, //g' openvswitch-2.3.2/rhel/openvswitch.spec > openvswitch-2.3.2/rhel/openvswitch_no_kmod.spec
rpmbuild -bb openvswitch-2.3.2/rhel/openvswitch_no_kmod.spec
mkdir /etc/openvswitch
yum localinstall /home/ovs/rpmbuild/RPMS/x86_64/openvswitch-2.3.2-1.x86_64.rpm
service openvswitch start
