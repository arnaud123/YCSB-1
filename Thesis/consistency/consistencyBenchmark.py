import subprocess;

from Thesis.ycsbClient.runMultipleYcsbClients import executeCommandOnYcsbNodes;
from Thesis.util.util import checkExitCodeOfProcess;
from Thesis.consistency.processConsistencyResult.FileParser import FileParser;
from Thesis.consistency.processConsistencyResult.TimeToConsistencyPlot import TimeToConsistencyPlot;
from Thesis.consistency.processConsistencyResult.AmountOfSwapsPlot import AmountOfSwapsPlot;
from Thesis.consistency.processConsistencyResult.IncreasingLoadConsistencyPlot import IncreasingLoadConsistencyPlot

def runSingleLoadBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile, outputFile, 
                            readConsistencyLevel, writeConsistencyLevel, requestPeriod, retryDelay, timeout, 
                            maxDelayBeforeDrop, stopOnFirstConsistency, amountOfReadThreads, workloadThreads):
    prepareDatabaseForBenchmark(cluster, pathForWorkloadFile);
    rawDataPaths = runBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile, outputFile, readConsistencyLevel, 
                writeConsistencyLevel, requestPeriod, retryDelay, timeout, maxDelayBeforeDrop, stopOnFirstConsistency, 
                amountOfReadThreads, workloadThreads);
    plotResults(rawDataPaths[0], outputFile + '_insert', amountOfReadThreads, timeout);
    plotResults(rawDataPaths[1], outputFile + '_update', amountOfReadThreads, timeout);

def runIncreasingLoadBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile, outputFile, 
                            readConsistencyLevel, writeConsistencyLevel, requestPeriod, retryDelay, timeout, 
                            maxDelayBeforeDrop, stopOnFirstConsistency, amountOfReadThreads, workloadThreads, listOfTargetThroughputs):
    rawDataPathsInsert = [];
    rawDataPathsUpdate = [];
    for targetThroughput in listOfTargetThroughputs:
        prepareDatabaseForBenchmark(cluster, pathForWorkloadFile);
        outputFileCurrentTest = outputFile + '_throughput_' + targetThroughput;
        rawDataPaths = runBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile, outputFileCurrentTest, 
                            readConsistencyLevel, writeConsistencyLevel, requestPeriod, retryDelay, timeout, 
                            maxDelayBeforeDrop, stopOnFirstConsistency, amountOfReadThreads, workloadThreads, int(targetThroughput));
        rawDataPathsInsert.append(rawDataPaths[0]);
        rawDataPathsUpdate.append(rawDataPaths[1]);
    plotter = IncreasingLoadConsistencyPlot(listOfTargetThroughputs, amountOfReadThreads, timeout);
    plotter.plot(rawDataPathsInsert, rawDataPathsUpdate, outputFile);

def prepareDatabaseForBenchmark(cluster, pathForWorkloadFile):
    cluster.writeConsistencyWorkloadFile([], pathForWorkloadFile);
    cluster.deleteDataInCluster();
    loadDatabase(cluster, pathForWorkloadFile);

def loadDatabase(cluster, pathForWorkloadFile):
    extraParameters = ['-p', 'consistencyTest=False'];
    loadCommand = cluster.getLoadCommand(pathForWorkloadFile, extraParameters);
    exitcode = subprocess.call(loadCommand);
    checkExitCodeOfProcess(exitcode, 'Loading database failed');

def runBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile, outputFile, 
                            readConsistencyLevel, writeConsistencyLevel, requestPeriod, retryDelay, timeout, 
                            maxDelayBeforeDrop, stopOnFirstConsistency, amountOfReadThreads, workloadThreads, targetThroughput=None):
    pathRawUpdateData = outputFile + '_updateRawData';
    pathRawInsertData = outputFile + '_insertRawData';
    extraParameters = [];
    extraParameters.extend(['-p', 'insertMatrixDelayExportFile=' + outputFile + '_insertDelay']);
    extraParameters.extend(['-p', 'updateMatrixDelayExportFile=' + outputFile + '_updateDelay']);
    extraParameters.extend(['-p', 'insertMatrixNbOfChangesExportFile=' + outputFile + '_insertNbOfChanges']);
    extraParameters.extend(['-p', 'updateMatrixNbOfChangesExportFile=' + outputFile + '_updateNbOfChanges']);
    extraParameters.extend(['-p', 'insertMatrixRawExportFile=' + pathRawInsertData]);
    extraParameters.extend(['-p', 'updateMatrixRawExportFile=' + pathRawUpdateData]);
    extraParameters.extend(['-p', 'cassandra.readconsistencylevel=' + str(readConsistencyLevel)]);
    extraParameters.extend(['-p', 'cassandra.writeconsistencylevel=' + str(writeConsistencyLevel)]);
    extraParameters.extend(['-p', 'newrequestperiodMillis=' + str(requestPeriod)]);
    extraParameters.extend(['-p', 'consistencyDelayMillis=' + str(retryDelay)]);
    extraParameters.extend(['-p', 'timeoutConsistencyBeforeDropInMicros=' + str(timeout)]);
    if(maxDelayBeforeDrop > 0):
        extraParameters.extend(['-p', 'maxDelayConsistencyBeforeDropInMicros=' + str(maxDelayBeforeDrop)]);
    extraParameters.extend(['-p', 'stopOnFirstConsistency=' + str(stopOnFirstConsistency)]);
    extraParameters.extend(['-p', 'readThreads=' + str(amountOfReadThreads)]);
    # The first IP  is the default of the database library
    # The second IP will be used for for write data is the consistency tests
    # This makes the database library use a different node for write and read operations
    extraParameters.extend(['-p', 'writenode=' + cluster.getNodesInCluster()[1]]);
    if(workloadThreads > 0):
        extraParameters.extend(['-p', 'addSeparateWorkload=True']);
    else:
        extraParameters.extend(['-p', 'addSeparateWorkload=False']);
        # Amount of threads has to be a positive number
        extraParameters.extend(['-threads', '1']);
    if(not targetThroughput is None):
        extraParameters.extend(['-target', str(targetThroughput)]);
    localRunCommand = cluster.getRunCommand(pathForWorkloadFile, runtimeBenchmarkInMinutes, str(workloadThreads), extraParameters);
    executeCommandOnYcsbNodes(localRunCommand, localRunCommand, outputFile + '_ycsb_result', []);
    return [pathRawInsertData, pathRawUpdateData];
    
def plotResults(inputFile, outputTemplate, amountOfReadThreads, timeout):
    fileParser = FileParser();
    dataAboutConsistency = fileParser.parse(inputFile, amountOfReadThreads, timeout);
    # plot stages to consistency
    timeToConsistencyPlot = TimeToConsistencyPlot(dataAboutConsistency);
    timeToConsistencyPlot.plotEarliestConsistentcy(outputTemplate + '_earliest');
    timeToConsistencyPlot.plotLatestConsistency(outputTemplate + '_latest');
    timeToConsistencyPlot.plotEarliestAndLatestConsistency(outputTemplate + '_combined');
    # plot amount of swaps in consistent inconsistent values
    amountOfSwapsPlot = AmountOfSwapsPlot(dataAboutConsistency);
    amountOfSwapsPlot.plot(outputTemplate + '_swaps');