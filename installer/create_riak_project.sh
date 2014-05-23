#!/bin/bash

# Create main files and directories
cd /root/YCSB/imp-projects
mkdir riak_project
cd riak_project
cat > .imp <<EOF
[config]
lib-dir = libs
export = 
EOF
mkdir libs
# Add required modules to libs directory
cd libs
git clone https://github.com/arnaud123/imp-riak.git riak
for mod in net ip redhat std; do
    git clone https://github.com/bartv/imp-$mod.git $mod
done
# Write main.cf
cd ..
cat > main.cf <<EOF
vm1 = ip::Host(name = "host1", os = "fedora-18", ip = "172.16.33.2")
vm2 = ip::Host(name = "host2", os = "fedora-18", ip = "172.16.33.3")

node1 = riak::Riak(host = vm1)
node2 = riak::Riak(host = vm2)

riak::Cluster(servers = [node1, node2])
EOF
