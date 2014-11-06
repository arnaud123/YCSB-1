import subprocess;

from delete_data.deleteAllRiakData import deleteAllDataInRiak;
from util.util import executeCommandOverSsh;
from cluster.Cluster import Cluster


class RiakCluster(Cluster):
    
    def __init__(self, normalBinding, consistencyBinding, nodesInCluster):
        super().__init__(normalBinding, consistencyBinding, nodesInCluster)
    
    def deleteDataInCluster(self):
        deleteAllDataInRiak(self.getNodesInCluster());

    def doRemoveNode(self, ipNodeToRemove):
        commandToExecute = "su riak -c 'riak-admin cluster leave riak@" + ipNodeToRemove + "; riak-admin cluster plan; riak-admin cluster commit'";
        return subprocess.Popen(["ssh", "root@" + ipNodeToRemove, commandToExecute]);

    def doAddNode(self, ipNodeToAdd):
        seedIp = self.getOtherIpInCluster(ipNodeToAdd);
        commandToExecute = "su riak -c 'riak start; riak-admin cluster join riak@" + seedIp + "; riak-admin cluster plan; riak-admin cluster commit'";
        executeCommandOverSsh(ipNodeToAdd, commandToExecute);
        
    def stopNode(self, ipNodeToStop):
        return subprocess.Popen(["ssh", "root@" + ipNodeToStop, "su riak -c 'riak stop'"]);

    def startNode(self, ipNodeToStart):
        executeCommandOverSsh(ipNodeToStart, "su riak -c 'riak start'");