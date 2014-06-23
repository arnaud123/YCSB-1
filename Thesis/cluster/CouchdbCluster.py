import subprocess;

from Thesis.cluster.Cluster import Cluster;
from Thesis.util.util import executeCommandOverSsh;
from Thesis.delete_data.deleteAllCouchdbData import deleteAllDataInCouchdb;

class CouchdbCluster(Cluster):
    
    def __init__(self, normalBinding, consistencyBinding, nodesInCluster):
        Cluster.__init__(self, normalBinding, consistencyBinding, nodesInCluster);
        self.__databaseName = 'usertable';
        self.__pathTmpWorkloadFile = '/tmp/tmpWorkloadFile';
    
    def deleteDataInCluster(self):
        deleteAllDataInCouchdb(self.getNodesInCluster(), self.__databaseName);

    def doRemoveNode(self, ipNodeToRemove):
        raise Exception('Unsupported operation');

    def doAddNode(self, ipNodeToAdd):
        raise Exception('Unsupported operation');
    
    def stopNode(self, ipNodeToStop):
        return subprocess.Popen(["ssh", "root@" + ipNodeToStop, "systemctl stop couchdb"]);

    def startNode(self, ipNodeToStart):
        executeCommandOverSsh(ipNodeToStart, "systemctl start couchdb");