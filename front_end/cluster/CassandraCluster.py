import subprocess

from delete_data.deleteAllCassandraData import clearCassandraKeyspace
from util.util import executeCommandOverSsh
from cluster.Cluster import Cluster

class CassandraCluster(Cluster):
    
    def __init__(self, normalBinding, consistencyBinding, nodesInCluster, readConsistencyLevel="QUORUM",
                 writeConsistencyLevel="QUORUM"):
        super().__init__(normalBinding, consistencyBinding, nodesInCluster)
        self._readConsistencyLevel = readConsistencyLevel
        self._writeConsistencyLevel = writeConsistencyLevel
    
    def deleteDataInCluster(self):
        clearCassandraKeyspace(self.getNodesInCluster())

    def doRemoveNode(self, ipNodeToRemove):
        return subprocess.Popen(["ssh", "root@" + ipNodeToRemove, "nodetool decommission"])

    def doAddNode(self, ipNodeToAdd):
        executeCommandOverSsh(ipNodeToAdd, "systemctl stop cassandra rm -rf /var/lib/cassandra/commitlog/* rm -rf /var/lib/cassandra/data/* rm -rf /var/lib/cassandra/saved_caches/* systemctl start cassandra")
        
    def stopNode(self, ipNodeToStop):
        return subprocess.Popen(["ssh", "root@" + ipNodeToStop, "systemctl stop cassandra"])

    def startNode(self, ipNodeToStart):
        executeCommandOverSsh(ipNodeToStart, "systemctl start cassandra")

    def addDbSpecificConsistencyBenchmarkParams(self, paramList):
        paramList.extend(['-p', 'cassandra.readconsistencylevel=' + self._readConsistencyLevel])
        paramList.extend(['-p', 'cassandra.writeconsistencylevel=' + self._writeConsistencyLevel])
        return paramList