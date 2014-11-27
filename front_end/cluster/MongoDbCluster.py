
from cluster.Cluster import Cluster
from delete_data.deleteAllMongoDbData import deleteAllDataInMongoDb

class MongoDbCluster(Cluster):

    _MAX_AMOUNT_OF_CONNECTION = 200

    def __init__(self, normalBinding, consistencyBinding, nodesInCluster, accessNodes,
                 writeConcern="safe", readPreference="primary"):
        super().__init__(normalBinding, consistencyBinding, nodesInCluster)
        self.__databaseName = "ycsb"
        self.__collectionName = "usertable"
        self._accessNodes = accessNodes
        self._writeConcern = writeConcern
        self._readPreference = readPreference

    def getLoadCommand(self, pathToWorkloadFile, extraParameters = []):
        extraParameters = self._addMongoDbSpecificProperties(extraParameters);
        return super(MongoDbCluster, self).getLoadCommand(pathToWorkloadFile, extraParameters);

    def getRunCommand(self, pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, extraParameters = []):
        extraParameters = self._addMongoDbSpecificProperties(extraParameters);
        return super(MongoDbCluster, self).getRunCommand(pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, extraParameters);

    def _addMongoDbSpecificProperties(self, paramList):
        paramList = self._addUrlPropertyToDbBinding(paramList)
        paramList = self._addAmountOfConnectionsToDbBinding(paramList)
        paramList = self._addWriteConcern(paramList)
        paramList = self._addReadPreference(paramList)
        return paramList

    def _addUrlPropertyToDbBinding(self, paramList):
        paramList.extend(['-p', "mongodb.url=mongodb://" + self._accessNodes[0] + ":27017"])
        return paramList

    def _addAmountOfConnectionsToDbBinding(self, paramList):
        paramList.extend(['-p', "mongodb.maxconnections=" + str(MongoDbCluster._MAX_AMOUNT_OF_CONNECTION)])
        return paramList

    def _addWriteConcern(self, paramList):
        paramList.extend(['-p', "mongodb.writeConcern=" + self._writeConcern])
        return paramList

    def _addReadPreference(self, paramList):
        paramList.extend(['-p', "mongodb.readPreference=" + self._readPreference])
        return paramList

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