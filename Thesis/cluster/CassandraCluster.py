import subprocess;

from Thesis.delete_data.deleteAllCassandraData import clearCassandraColumnFamily;
from Thesis.cluster.Cluster import Cluster;
from Thesis.util.util import executeCommandOverSsh;

class CassandraCluster(Cluster):
    
    def __init__(self, normalBinding, consistencyBinding, nodesInCluster):
        Cluster.__init__(self, normalBinding, consistencyBinding, nodesInCluster);
    
    def deleteDataInCluster(self):
        clearCassandraColumnFamily(self.getNodesInCluster());

    def doRemoveNode(self, ipNodeToRemove):
        return subprocess.Popen(["ssh", "root@" + ipNodeToRemove, "nodetool decommission"]);

    def doAddNode(self, ipNodeToAdd):
        executeCommandOverSsh(ipNodeToAdd, "systemctl stop cassandra; rm -rf /var/lib/cassandra/commitlog/*; rm -rf /var/lib/cassandra/data/*; rm -rf /var/lib/cassandra/saved_caches/*; systemctl start cassandra");
        
    def stopNode(self, ipNodeToStop):
        return subprocess.Popen(["ssh", "root@" + ipNodeToStop, "systemctl stop cassandra"]);

    def startNode(self, ipNodeToStart):
        executeCommandOverSsh(ipNodeToStart, "systemctl start cassandra");