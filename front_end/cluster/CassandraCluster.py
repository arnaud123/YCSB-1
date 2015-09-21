import subprocess

from delete_data.deleteAllCassandraData import clearCassandraKeyspace
from util.util import executeCommandOverSsh
from cluster.Cluster import Cluster

class CassandraCluster(Cluster):
    
    def __init__(self, normalBinding, consistencyBinding, nodesInCluster,
                 readConsistencyLevel, writeConsistencyLevel):
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

    def getConsistencyRunCommand(self, pathToWorkloadFile, pathConsistencyResult, runtimeBenchmarkInMinutes,
                                 workloadThreads, outputFile, requestPeriod, seedForOperationSelection,
                                 accuracyInMicros, maxDelayBeforeDrop, stopOnFirstConsistency, cluster,
                                 targetThroughput, pathRawInsertData, pathRawUpdateData, delayToWriterThreadInMicros, extraParameters = []):
        extraParameters = self._addConsistencyLevelsToParams(extraParameters)
        extraParameters = self._addWriteNodeParameter(extraParameters)
        return super().getConsistencyRunCommand(pathToWorkloadFile, pathConsistencyResult, runtimeBenchmarkInMinutes,
                                 workloadThreads, outputFile, requestPeriod, seedForOperationSelection,
                                 accuracyInMicros, maxDelayBeforeDrop, stopOnFirstConsistency, cluster,
                                 targetThroughput, pathRawInsertData, pathRawUpdateData, delayToWriterThreadInMicros, extraParameters)

    def getLoadCommand(self, pathToWorkloadFile, extraParameters = []):
        extraParameters = self._addConsistencyLevelsToParams(extraParameters)
        extraParameters = self._addWriteNodeParameter(extraParameters)
        return super().getLoadCommand(pathToWorkloadFile, extraParameters)

    def getRunCommand(self, pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, extraParameters = []):
        extraParameters = self._addConsistencyLevelsToParams(extraParameters)
        extraParameters = self._addWriteNodeParameter(extraParameters)
        return super().getRunCommand(pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, extraParameters)

    def _addConsistencyLevelsToParams(self, params):
        params.extend(['-p', 'cassandra.readconsistencylevel=' + self._readConsistencyLevel])
        params.extend(['-p', 'cassandra.writeconsistencylevel=' + self._writeConsistencyLevel])
        return params

    def _addWriteNodeParameter(self, params):
        params.extend(['-p', 'writenode=' + self.getNodesInCluster()[1]])
        return params