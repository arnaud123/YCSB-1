#/bin/bash

# Install IMP
/root/YCSB/installer/install_imp.sh
# Install IMP modules
cd /root/YCSB/
mkdir imp-modules
/root/YCSB/installer/create_cassandra_project.sh
/root/YCSB/installer/create_couchdb_project.sh
/root/YCSB/installer/create_mysqlCluster_project.sh
/root/YCSB/installer/create_riak_project.sh
# Install R
yum -y install R
# Disable firewall
setenforce 0
sed -i "s/SELINUX=enforcing/SELINUX=permissive/g" /etc/sysconfig/selinux
systemctl disable firewalld
# create ssh-keys
ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa
