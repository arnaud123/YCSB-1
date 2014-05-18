#!/bin/bash

# Create main files and directories
cd /root/YCSB/imp-modules
mkdir mysqlCluster_project
cd mysqlCluster_project
cat > .imp <<EOF
[config]
lib-dir = libs
export = 
EOF
mkdir libs
# Add required modules to libs directory
cd libs
git clone https://github.com/arnaud123/imp-mysqlCluster.git mysqlCluster
for mod in net ip redhat std; do
    git clone https://github.com/bartv/imp-$mod.git $mod
done
# Write main.cf
cd ..
cat > main.cf <<EOF
vm1 = ip::Host(name = "test1", os = "fedora-18", ip = "172.16.33.6")
vm2 = ip::Host(name = "test2", os = "fedora-18", ip = "172.16.33.7")

node1 = mysqlCluster::MasterNode(host = vm1, id = 1)
node2 = mysqlCluster::SlaveNode(host = vm2, id = 2)

database = mysqlCluster::Database(name = "drupal_test", user = "drupal_test", 
					password = "Str0ng-P433w0rd")

mysqlCluster::Cluster(master = node1, slaves =  [node2], databases = database)
EOF
