#!/bin/bash

# Create main files and directories
cd /root/YCSB/imp-modules
mkdir cassandra_project
cd cassandra_project
cat > .imp <<EOF
[config]
lib-dir = libs
export = 
EOF
mkdir libs
# Add required modules to libs directory
cd libs
git clone https://github.com/arnaud123/imp-cassandra.git cassandra
for mod in net ip redhat std java yum; do
    git clone https://github.com/bartv/imp-$mod.git $mod
done
# Write main.cf
cd ..
cat > main.cf <<EOF
vm1 = ip::Host(name = "vm1", os = "fedora-18", ip = "172.16.33.2")
vm2 = ip::Host(name = "vm2", os = "fedora-18", ip = "172.16.33.4")

node1 = cassandra::Cassandra(host = vm1, jmx_enabled = false)
node2 = cassandra::Cassandra(host = vm2, jmx_enabled = false)

cassandra::Cluster(name = "eenTestCluster", servers = [node1, node2])
EOF
