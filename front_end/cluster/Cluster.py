import subprocess;

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
        dataToWrite = 'recordcount=10000\n' + \
        'operationcount=10000000\n' + \
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
        dataToWrite = """recordcount=10000
operationcount=10000000
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

    def getConsistencyRunCommand(self, pathToWorkloadFile, pathConsistencyResult, runtimeBenchmarkInSeconds, amountOfThreads, extraParameters = []):
        extraParameters.extend(['-p', 'resultfile=' + pathConsistencyResult]);
        return getRunCommand(self.getConsistencyBinding(), pathToWorkloadFile, runtimeBenchmarkInSeconds, amountOfThreads, extraParameters);

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
        raise Exception('No other ip found in cluster');