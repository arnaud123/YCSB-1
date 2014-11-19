import subprocess;
import math

from util.ycsbCommands.Commands import getLoadCommand;
from util.ycsbCommands.Commands import getRunCommand;
from util.util import checkExitCodeOfProcess;

class Cluster(object):
    
    def __init__(self, normalBinding, consistencyBinding, nodesInCluster):
        self.__normalbinding = normalBinding;
        self.__consistencyBinding = consistencyBinding;
        self.__nodesInCluster = nodesInCluster;
        
    def getNormalBinding(self):
        return self.__normalbinding;
    
    def getConsistencyBinding(self):
        return self.__consistencyBinding;
    
    def getNodesInCluster(self):
        return list(self.__nodesInCluster);
        
    # Should be overriden in subclasses
    def deleteDataInCluster(self):
        pass;
    
    def writeNormalWorkloadFile(self, remoteYcsbNodes, pathForWorkloadFile):
        dataToWrite = 'recordcount=100000\n' + \
        'operationcount=100000000\n' + \
        """workload=com.yahoo.ycsb.workloads.CoreWorkload
    
readallfields=true
    
readproportion=0.4
updateproportion=0.25
scanproportion=0.1
insertproportion=0.25

scanlengthdistribution=uniform
maxscanlength=100
 
requestdistribution=zipfian

hosts=""" + ",".join(self.getNodesInCluster());
        self.writeFileToYcsbNodes(dataToWrite, remoteYcsbNodes, pathForWorkloadFile, pathForWorkloadFile);

    def writeConsistencyWorkloadFile(self, remoteYcsbNodes, pathForWorkloadFile):
        dataToWrite = """recordcount=100000
operationcount=100000000
workload=com.yahoo.ycsb.workloads.CoreWorkload

readallfields=true

readproportion=0.4
updateproportion=0.25
scanproportion=0.1
insertproportion=0.25

scanlengthdistribution=uniform
maxscanlength=100

requestdistribution=zipfian

starttime=10000

consistencyTest=True

useFixedOperationDistributionSeed=True
operationDistributionSeed=46732463246

readProportionConsistencyCheck=0.5
updateProportionConsistencyCheck=0.5

hosts=""" + ",".join(self.getNodesInCluster());
        self.writeFileToYcsbNodes(dataToWrite, remoteYcsbNodes, pathForWorkloadFile, pathForWorkloadFile);

    def writeFileToYcsbNodes(self, dataToWrite, remoteYcsbNodes, localPath, remotePath):
        f = open(localPath, "w");
        f.write(dataToWrite);
        f.close();
        for ip in remoteYcsbNodes:
            exitCode = subprocess.call(['scp', localPath, 'root@' + ip + ':' + remotePath]);
            checkExitCodeOfProcess(exitCode, 'Writing workload file to remote YCSB nodes failed');

    def getLoadCommand(self, pathToWorkloadFile, extraParameters = []):
        return getLoadCommand(self.getNormalBinding(), pathToWorkloadFile, extraParameters);

    def getRunCommand(self, pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, extraParameters = []):
        return getRunCommand(self.getNormalBinding(), pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, extraParameters);

    def getConsistencyRunCommand(self, pathToWorkloadFile, pathConsistencyResult, runtimeBenchmarkInMinutes,
                                 workloadThreads, outputFile, requestPeriod, seedForOperationSelection,
                                 accuracyInMicros, maxDelayBeforeDrop, stopOnFirstConsistency, cluster,
                                 targetThroughput, pathRawInsertData, pathRawUpdateData, extraParameters = []):
        extraParameters = self.addDbSpecificConsistencyBenchmarkParams(extraParameters)
        extraParameters.extend(['-p', 'insertMatrixDelayExportFile=' + outputFile + '_insertDelay'])
        extraParameters.extend(['-p', 'updateMatrixDelayExportFile=' + outputFile + '_updateDelay'])
        extraParameters.extend(['-p', 'insertMatrixNbOfChangesExportFile=' + outputFile + '_insertNbOfChanges'])
        extraParameters.extend(['-p', 'updateMatrixNbOfChangesExportFile=' + outputFile + '_updateNbOfChanges'])
        extraParameters.extend(['-p', 'insertMatrixRawExportFile=' + pathRawInsertData])
        extraParameters.extend(['-p', 'updateMatrixRawExportFile=' + pathRawUpdateData])
        extraParameters.extend(['-p', 'newrequestperiodMillis=' + str(requestPeriod)])
        extraParameters.extend(['-p', 'timeoutConsistencyBeforeDropInMicros=100000000'])  # neglect field
        extraParameters.extend(["-p", "useFixedOperationDistributionSeed=True"])
        extraParameters.extend(["-p", "operationDistributionSeed=" + seedForOperationSelection])
        extraParameters.extend(["-p", "accuracyInMicros=" + str(accuracyInMicros)])
        if(maxDelayBeforeDrop > 0):
            extraParameters.extend(['-p', 'maxDelayConsistencyBeforeDropInMicros=' + str(maxDelayBeforeDrop)])
        extraParameters.extend(['-p', 'stopOnFirstConsistency=' + str(stopOnFirstConsistency)])
        # The first IP  is the default of the database library
        # The second IP will be used for for write data is the consistency tests
        # This makes the database library use a different node for write and read operations
        extraParameters.extend(['-p', 'writenode=' + cluster.getNodesInCluster()[1]])
        if targetThroughput is not None:
            targetThroughputLoadThreads = self._getTargetThroughputLoadThreads(requestPeriod, accuracyInMicros,
                                                                               targetThroughput)
            if targetThroughputLoadThreads > 0:
                extraParameters.extend(['-p', 'addSeparateWorkload=True'])
                extraParameters.extend(['-threads', str(workloadThreads)])
                extraParameters.extend(['-target', str(targetThroughputLoadThreads)])
            else:
                extraParameters.extend(['-p', 'addSeparateWorkload=False'])
        extraParameters.extend(['-p', 'resultfile=' + pathConsistencyResult])
        return getRunCommand(self.getConsistencyBinding(), pathToWorkloadFile, runtimeBenchmarkInMinutes,
                             str(workloadThreads), extraParameters)

    def addDbSpecificConsistencyBenchmarkParams(self, paramList):
        return paramList

    def _getTargetThroughputLoadThreads(self, requestPeriodInMillis, accuracyInMicros, targetThroughput):
        throughputNonLoadThreads = self._getThroughputProducedByNonLoadThreads(requestPeriodInMillis, accuracyInMicros)
        return max(targetThroughput - throughputNonLoadThreads, 0)

    def _getThroughputProducedByNonLoadThreads(self, requestPeriodInMillis, accuracyInMicros):
        requestPeriodsPerSecond = (1000/requestPeriodInMillis)
        writesPerSecond = requestPeriodsPerSecond
        requestPeriodInMicros = requestPeriodInMillis*1000
        readsPerRequestPeriod = math.ceil(requestPeriodInMicros/accuracyInMicros)
        readsPerSecond = requestPeriodsPerSecond * readsPerRequestPeriod
        return int(writesPerSecond + readsPerSecond)

    def removeNode(self, ipNodeToRemove):
        result = self.doRemoveNode(ipNodeToRemove);
        self.__nodesInCluster.remove(ipNodeToRemove);
        return result;

    def addNode(self, ipNodeToAdd):
        self.doAddNode(ipNodeToAdd);
        self.__nodesInCluster.append(ipNodeToAdd);
        
    # Should be overriden in subclasses
    def stopNode(self, ipNodeToStop):
        pass;

    # Should be overriden in subclasses
    def startNode(self, ipNodeToStart):
        pass;
    
    def getOtherIpInCluster(self, ip):
        for otherIp in self.__nodesInCluster:
            if otherIp != ip:
                return otherIp;
        raise Exception('No other ip found in cluster')