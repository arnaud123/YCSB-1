import subprocess;

from util.util import executeCommandOverSsh;
from delete_data.deleteAllCouchdbData import deleteAllDataInCouchdb;
from cluster import Cluster


class CouchdbCluster(Cluster):
    
    def __init__(self, normalBinding, consistencyBinding, nodesInCluster):
        super().__init__(normalBinding, consistencyBinding, nodesInCluster);
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