#/bin/bash

# Install IMP
/root/YCSB/installer/install_imp.sh
# Install IMP modules
cd /root/YCSB/
mkdir imp-projects
/root/YCSB/installer/create_cassandra_project.sh
/root/YCSB/installer/create_couchdb_project.sh
/root/YCSB/installer/create_mysqlCluster_project.sh
/root/YCSB/installer/create_riak_project.sh
# Install R and maven
yum -y install R maven
# Build YCSB
mvn clean package
