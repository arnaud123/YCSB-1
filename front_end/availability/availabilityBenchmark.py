import subprocess;

from util.util import checkExitCodeOfProcess;
from ycsbClient.runMultipleYcsbClients import executeCommandOnYcsbNodes;
from plot.ParseYcsbTestResults import parseAndPlot;

def runAvailabilityBenchmark(cluster, remoteYcsbNodes, pathToWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, 
                          amountOfThreads, eventFile, targetThroughput = None):
    # Clear database
    cluster.deleteDataInCluster();
    cluster.writeNormalWorkloadFile(remoteYcsbNodes, pathToWorkloadFile);
    # Load database
    loadDatabase(cluster, pathToWorkloadFile); 
    # Start benchmark
    runBenchmark(cluster, pathToWorkloadFile, runtimeBenchmarkInMinutes, pathBenchmarkResult, remoteYcsbNodes, 
                 amountOfThreads, targetThroughput, eventFile);
    parseAndPlot(pathBenchmarkResult);

def loadDatabase(cluster, pathForWorkloadFile):
    loadCommand = cluster.getLoadCommand(pathForWorkloadFile);
    exitcode = subprocess.call(loadCommand);
    checkExitCodeOfProcess(exitcode, 'Loading database failed');
    
def runBenchmark(cluster, pathToWorkloadFile, runtimeBenchmarkInMinutes, pathBenchmarkResult, remoteYcsbClientIps, 
                 amountOfThreads, targetThroughput, eventFile):
    extraParams = ['-p', 'eventFile=' + eventFile]
    if targetThroughput is None:
        localRunCommand = cluster.getRunCommand(pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, extraParams);    
    else:
        extraParams.extend(['-target', targetThroughput]);
        localRunCommand = cluster.getRunCommand(pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, extraParams);
    executeCommandOnYcsbNodes(localRunCommand, localRunCommand, pathBenchmarkResult, remoteYcsbClientIps);