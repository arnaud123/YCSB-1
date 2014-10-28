#!/bin/python

import subprocess;
from time import sleep;

from load.process_result.AggregatedBenchmarkResult import AggregatedBenchmarkResult;
from util.util import checkExitCodeOfProcess;
from ycsbClient.runMultipleYcsbClients import executeCommandOnYcsbNodes;

LOAD_PLOT_SCRIPT = '/root/YCSB/front_end/plot/plot_loads'

def runLoadBenchmark(cluster, remoteYcsbNodes, pathToWorkloadFile, runtimeBenchmarkInMinutes, fileToWriteResultTo, amountOfThreads, opsPerSec):
    cluster.writeNormalWorkloadFile(remoteYcsbNodes, pathToWorkloadFile);
    cluster.deleteDataInCluster();
    # Load database
    loadCommand = cluster.getLoadCommand(pathToWorkloadFile);
    exitCode = subprocess.call(loadCommand);
    checkExitCodeOfProcess(exitCode, 'Loading database failed');
    # Run benchmark
    runCommand = cluster.getRunCommand(pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads, ['-target', opsPerSec]);
    executeCommandOnYcsbNodes(runCommand, runCommand, fileToWriteResultTo, remoteYcsbNodes);
    return aggregateResults(remoteYcsbNodes, fileToWriteResultTo);

def runLoadBenchmarkAsBatch(cluster, remoteYcsbNodes, pathToWorkloadFile, runtimeBenchmarkInMinutes, dirToWriteResultTo, 
                            listOfOpsPerSec, listOfAmountThreads, listOfAmountOfMachines):
    dirToWriteResultTo = dirToWriteResultTo.rstrip('/');
    for amountOfMachines in listOfAmountOfMachines:
        for amountOfThreads in listOfAmountThreads:
            aggResults = [];
            for opsPerSec in listOfOpsPerSec:
                filenameResult = getFilenameResultFile(dirToWriteResultTo, amountOfMachines, amountOfThreads, opsPerSec);
                newResult = runLoadBenchmark(cluster, remoteYcsbNodes[0:int(amountOfMachines)-1], pathToWorkloadFile, runtimeBenchmarkInMinutes, filenameResult, amountOfThreads, opsPerSec);
                aggResults.append(newResult);
            filenameAggResult = getFilenameAggResultFile(dirToWriteResultTo, amountOfMachines, amountOfThreads);
            printMergedAggResultsToFile(aggResults, listOfOpsPerSec, filenameAggResult);
            sleep(30);
            subprocess.call(['Rscript', LOAD_PLOT_SCRIPT, filenameAggResult, filenameAggResult]);

def getFilenameResultFile(directory, amountOfMachines, amountOfThreads, amountOfOperations):
    return directory + '/' + amountOfMachines + '_machines_' + amountOfThreads + '_threads_' + amountOfOperations + '_ops';

def getFilenameAggResultFile(directory, amountOfMachines, amountOfThreads):
    return directory + '/' +amountOfMachines + '_machines_' + amountOfThreads + '_threads_RESULT';

def aggregateResults(ipsRemoteYcsbClient, pathResultFile):
    resultPaths = copyResultFilesToLocal(ipsRemoteYcsbClient, pathResultFile);
    resultPaths.append(pathResultFile);
    return AggregatedBenchmarkResult(resultPaths);

def copyResultFilesToLocal(listOfIps, remotePath):
    pathsNewCopiedFiles = [];
    for ip in listOfIps:
        pathNewLocalFile = remotePath + '_' + ip;
        pathsNewCopiedFiles.append(pathNewLocalFile);
        exitCode = subprocess.call(['scp', 'root@' + ip + ':/root/YCSB/result', pathNewLocalFile]);
        checkExitCodeOfProcess(exitCode, 'Failed to copy result files from remote ycsb clients to local machine');
    return pathsNewCopiedFiles;

# def printMergedAggResultsToFile(listOfAggResults, pathResultFile):
#     f = open(pathResultFile, 'w');
#     for operation in ['AverageReadLatency', 'AverageInsertLatency', 'AverageUpdateLatency', 
#                       'AverageScanLatency', 'AverageDeleteLatency']:
#         f.write('=== ' + operation + ' ===\n');
#         for aggResult in listOfAggResults:
#             f.write(str(aggResult.getThroughput()) + ', ' + str(aggResult.getAggregatedLatency(operation)) + '\n');
#     f.close();

def printMergedAggResultsToFile(listOfAggResults, expectedThroughput, pathResultFile):
    f = open(pathResultFile, 'w');
    f.write('expected_throughput, real_throughput, latency\n');
    indexCounter = 0;
    for aggResult in listOfAggResults:
        latency = 0;
        counter = 0;
        for operation in ['AverageReadLatency', 'AverageInsertLatency', 'AverageUpdateLatency', 
                      'AverageScanLatency', 'AverageDeleteLatency']:
            if aggResult.getAggregatedLatency(operation) > 0:
                latency += aggResult.getAggregatedLatency(operation);
                counter += 1;
        if counter != 0:
            latency = latency/counter;
            f.write(str(expectedThroughput[indexCounter]) + ',' + str(aggResult.getThroughput()) + ', ' + str(latency) + '\n');
        indexCounter += 1;
    f.close();