import subprocess;

from time import sleep;
from threading import Thread;
from Thesis.util.util import checkExitCodeOfProcess;
from Thesis.ycsbClient.runMultipleYcsbClients import executeCommandOnYcsbNodes;
from Thesis.plot.ParseYcsbTestResults import parseAndPlot;

def runStopStartBenchmark(cluster, remoteYcsbNodes, IpNodeToBeKilled, pathForWorkloadFile, pathBenchmarkResult, 
                          runtimeBenchmarkInMinutes, killTimeInSeconds, startTimeInSeconds, amountOfThreads, targetThroughput = None):
    cluster.deleteDataInCluster();
    cluster.writeNormalWorkloadFile(remoteYcsbNodes, pathForWorkloadFile);
    loadDatabase(cluster, pathForWorkloadFile);
    benchmarkThread = runBenchmark(cluster, pathForWorkloadFile, runtimeBenchmarkInMinutes, pathBenchmarkResult, remoteYcsbNodes, 
                                   amountOfThreads, targetThroughput);
    # Kill node at kill time
    sleep(killTimeInSeconds);
    print "Stopping node: " + IpNodeToBeKilled;
    stopProcess = cluster.stopNode(IpNodeToBeKilled);
    # Start node at start at
    sleep(startTimeInSeconds - killTimeInSeconds);
    print "Starting node: " + IpNodeToBeKilled;
    cluster.startNode(IpNodeToBeKilled);
    # Wait for benchmark to finish
    benchmarkThread.join();
    stopProcess.communicate();
    checkExitCodeOfProcess(stopProcess.poll(), 'Stop node process failed');
    # Plot results
    parseAndPlot(pathBenchmarkResult);
    
def loadDatabase(cluster, pathForWorkloadFile):
    loadCommand = cluster.getLoadCommand(pathForWorkloadFile);
    exitcode = subprocess.call(loadCommand);
    checkExitCodeOfProcess(exitcode, 'Loading database failed');
    
def runBenchmark(cluster, pathToWorkloadFile, runtimeBenchmarkInMinutes, pathBenchmarkResult, remoteYcsbClientIps, 
                 amountOfThreads, targetThroughput):
    if targetThroughput is None:
        localRunCommand = cluster.getRunCommand(pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads);
    else:
        localRunCommand = cluster.getRunCommand(pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, ['-target', targetThroughput]);
    benchmarkThread = Thread(target=executeCommandOnYcsbNodes, args=(localRunCommand, localRunCommand, pathBenchmarkResult, remoteYcsbClientIps));
    benchmarkThread.start();
    return benchmarkThread;