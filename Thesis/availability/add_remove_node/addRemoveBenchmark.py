import time;
import subprocess;
from threading import Thread;

from Thesis.util.util import checkExitCodeOfProcess;
from Thesis.ycsbClient.runMultipleYcsbClients import executeCommandOnYcsbNodes;
from Thesis.plot.ParseYcsbTestResults import parseAndPlot;

def runAddRemoveBenchmark(cluster, remoteYcsbNodes, ipNodeToRemove, pathToWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, 
                          removeTimeInSeconds, addTimeInSeconds, amountOfThreads, targetThroughput = None):
    # Clear database
    cluster.deleteDataInCluster();
    cluster.writeNormalWorkloadFile(remoteYcsbNodes, pathToWorkloadFile);
    # Load database
    loadDatabase(cluster, pathToWorkloadFile); 
    # Start benchmark
    benchmarkThread = runBenchmark(cluster, pathToWorkloadFile, runtimeBenchmarkInMinutes, pathBenchmarkResult, remoteYcsbNodes, 
                                   amountOfThreads, targetThroughput);
    # Remove node at remove time
    time.sleep(removeTimeInSeconds);
    print "Removing node: " + ipNodeToRemove;
    removeProcess = cluster.removeNode(ipNodeToRemove);
    # Add node at add time
    time.sleep(addTimeInSeconds - removeTimeInSeconds);
    print "Adding node: " + ipNodeToRemove;
    cluster.addNode(ipNodeToRemove);
    # Wait for benchmark to finish
    benchmarkThread.join();
    removeProcess.communicate();
    checkExitCodeOfProcess(removeProcess.poll(), 'Node remove process failed');
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