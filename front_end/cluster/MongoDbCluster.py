
from cluster.Cluster import Cluster
from delete_data.deleteAllMongoDbData import deleteAllDataInMongoDb

class MongoDbCluster(Cluster):
    
    def __init__(self, normalBinding, consistencyBinding, nodesInCluster, accessNodes):
        super().__init__(normalBinding, consistencyBinding, nodesInCluster)
        self.__databaseName = "ycsb"
        self.__collectionName = "usertable"
        self._accessNodes = accessNodes
        
    def deleteDataInCluster(self):
        accessNode = self._accessNodes[0]
        deleteAllDataInMongoDb(accessNode, self.getNodesInCluster(), self.__databaseName, self.__collectionName)

    def doRemoveNode(self, ipNodeToRemove):
        raise Exception('Unsupported operation')

    def doAddNode(self, ipNodeToAdd):
        raise Exception('Unsupported operation')
    
    def stopNode(self, ipNodeToStop):
        raise Exception('Unsupported operation')

    def startNode(self, ipNodeToStart):
        raise Exception('Unsupported operation')