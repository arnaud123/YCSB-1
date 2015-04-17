__author__ = 'arnaud'

from cluster.Cluster import Cluster
from delete_data.deleteAllElasticsearchData import deleteAllElasticsearchData

class ElasticsearchCluster(Cluster):

    def __init__(self, normalBinding, consistencyBinding, nodesInCluster, clusterName):
        super().__init__(normalBinding, consistencyBinding, nodesInCluster)
        self.__clusterName = clusterName

    def deleteDataInCluster(self):
        ipNodeInCluster = self.getNodesInCluster()[0]
        deleteAllElasticsearchData(ipNodeInCluster)

    def doRemoveNode(self, ipNodeToRemove):
        raise Exception('Unsupported operation')

    def doAddNode(self, ipNodeToAdd):
        raise Exception('Unsupported operation')

    def stopNode(self, ipNodeToStop):
        raise Exception('Unsupported operation')

    def startNode(self, ipNodeToStart):
        raise Exception('Unsupported operation')

    def getConsistencyRunCommand(self, pathToWorkloadFile, pathConsistencyResult, runtimeBenchmarkInMinutes,
                                 workloadThreads, outputFile, requestPeriod, seedForOperationSelection,
                                 accuracyInMicros, maxDelayBeforeDrop, stopOnFirstConsistency, cluster,
                                 targetThroughput, pathRawInsertData, pathRawUpdateData, delayToWriterThreadInMicros, extraParameters = []):
        extraParameters = self.__addClusterNameParameter(extraParameters)
        return super().getConsistencyRunCommand(pathToWorkloadFile, pathConsistencyResult, runtimeBenchmarkInMinutes,
                                 workloadThreads, outputFile, requestPeriod, seedForOperationSelection,
                                 accuracyInMicros, maxDelayBeforeDrop, stopOnFirstConsistency, cluster,
                                 targetThroughput, pathRawInsertData, pathRawUpdateData, delayToWriterThreadInMicros, extraParameters)

    def getLoadCommand(self, pathToWorkloadFile, extraParameters = []):
        extraParameters = self.__addClusterNameParameter(extraParameters)
        return super().getLoadCommand(pathToWorkloadFile, extraParameters)

    def getRunCommand(self, pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, extraParameters = []):
        extraParameters = self.__addClusterNameParameter(extraParameters)
        return super().getRunCommand(pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, extraParameters)

    def __addClusterNameParameter(self, params):
        params.extend(['-p', 'es.ycsb.cluster=' + self.__clusterName])
        return params