#!/bin/bash

# Create main files and directories
cd /root/YCSB/imp-projects
mkdir couchdb_project
cd couchdb_project
cat > .imp <<EOF
[config]
lib-dir = libs
export = 
EOF
mkdir libs
# Add required modules to libs directory
cd libs
git clone https://github.com/arnaud123/imp-couchdb.git couchdb
for mod in net ip redhat std; do
    git clone https://github.com/bartv/imp-$mod.git $mod
done
# Write main.cf
cd ..
cat > main.cf <<EOF
vm1 = ip::Host(name = "host1", os = "fedora-18", ip = "172.16.33.2")
vm2 = ip::Host(name = "host2", os = "fedora-18", ip = "172.16.33.3")

node1 = couchdb::Couchdb(host = vm1)
node2 = couchdb::Couchdb(host = vm2)

database1 = couchdb::Database(name = "usertable")

couchdb::Cluster(servers = [node1, node2], databases = database1)
EOF
