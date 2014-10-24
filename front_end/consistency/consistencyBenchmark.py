import subprocess

from ycsbClient.runMultipleYcsbClients import executeCommandOnYcsbNodes
from util.util import checkExitCodeOfProcess
from consistency.processConsistencyResult.FileParser import FileParser
from consistency.processConsistencyResult.plotCdf import plotCdf

WARM_UP_TIME_IN_SECONDS = 120

def runSingleLoadBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile, outputFile,
                           readConsistencyLevel, writeConsistencyLevel, seedForOperationSelection, requestPeriod,
                           accuracyInMicros, timeout, maxDelayBeforeDrop, stopOnFirstConsistency, workloadThreads,
                           targetThroughputWorkloadThreads):
    prepareDatabaseForBenchmark(cluster, pathForWorkloadFile)
    (pathRawInsertData, pathRawUpdateData) = runBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile,
                                                          outputFile, readConsistencyLevel, writeConsistencyLevel,
                                                          seedForOperationSelection, requestPeriod, accuracyInMicros,
                                                          timeout, maxDelayBeforeDrop, stopOnFirstConsistency,
                                                          workloadThreads, targetThroughputWorkloadThreads)
    plotResults(pathRawInsertData, outputFile + '_insert')
    plotResults(pathRawUpdateData, outputFile + '_update')

def runIncreasingLoadBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile, outputFile,
                               readConsistencyLevel, writeConsistencyLevel, seedForOperationSelection, requestPeriod,
                               accuracyInMicros, timeout, maxDelayBeforeDrop, stopOnFirstConsistency, workloadThreads,
                               listOfTargetThroughputs):
    rawDataPathsInsert = []
    rawDataPathsUpdate = []
    for targetThroughput in listOfTargetThroughputs:
        prepareDatabaseForBenchmark(cluster, pathForWorkloadFile)
        outputFileCurrentTest = outputFile + '_throughput_' + targetThroughput
        (pathRawInsertData, pathRawUpdateData) = runBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile,
                                                              outputFileCurrentTest, readConsistencyLevel,
                                                              writeConsistencyLevel, seedForOperationSelection,
                                                              requestPeriod, accuracyInMicros, timeout,
                                                              maxDelayBeforeDrop, stopOnFirstConsistency,
                                                              workloadThreads, int(targetThroughput))
        rawDataPathsInsert.append(pathRawInsertData)
        rawDataPathsUpdate.append(pathRawUpdateData)
    # plotter = IncreasingLoadConsistencyPlot(listOfTargetThroughputs, amountOfReadThreads, timeout)
    # plotter.plot(rawDataPathsInsert, rawDataPathsUpdate, outputFile)

def prepareDatabaseForBenchmark(cluster, pathForWorkloadFile):
    cluster.writeConsistencyWorkloadFile([], pathForWorkloadFile)
    cluster.deleteDataInCluster()
    loadDatabase(cluster, pathForWorkloadFile)

def loadDatabase(cluster, pathForWorkloadFile):
    extraParameters = ['-p', 'consistencyTest=False']
    loadCommand = cluster.getLoadCommand(pathForWorkloadFile, extraParameters)
    exitcode = subprocess.call(loadCommand)
    checkExitCodeOfProcess(exitcode, 'Loading database failed')

def runBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile, outputFile,
                 readConsistencyLevel, writeConsistencyLevel, seedForOperationSelection, requestPeriod,
                 accuracyInMicros, timeout, maxDelayBeforeDrop, stopOnFirstConsistency, workloadThreads,
                 targetThroughput=None):
    pathRawUpdateData = outputFile + '_updateRawData'
    pathRawInsertData = outputFile + '_insertRawData'
    extraParameters = []
    extraParameters.extend(['-p', 'insertMatrixDelayExportFile=' + outputFile + '_insertDelay'])
    extraParameters.extend(['-p', 'updateMatrixDelayExportFile=' + outputFile + '_updateDelay'])
    extraParameters.extend(['-p', 'insertMatrixNbOfChangesExportFile=' + outputFile + '_insertNbOfChanges'])
    extraParameters.extend(['-p', 'updateMatrixNbOfChangesExportFile=' + outputFile + '_updateNbOfChanges'])
    extraParameters.extend(['-p', 'insertMatrixRawExportFile=' + pathRawInsertData])
    extraParameters.extend(['-p', 'updateMatrixRawExportFile=' + pathRawUpdateData])
    extraParameters.extend(['-p', 'cassandra.readconsistencylevel=' + str(readConsistencyLevel)])
    extraParameters.extend(['-p', 'cassandra.writeconsistencylevel=' + str(writeConsistencyLevel)])
    extraParameters.extend(['-p', 'newrequestperiodMillis=' + str(requestPeriod)])
    extraParameters.extend(['-p', 'timeoutConsistencyBeforeDropInMicros=' + str(timeout)])
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
    if(workloadThreads > 0):
        extraParameters.extend(['-p', 'addSeparateWorkload=True'])
    else:
        extraParameters.extend(['-p', 'addSeparateWorkload=False'])
        # Amount of threads has to be a positive number
        extraParameters.extend(['-threads', '1'])
    if(not targetThroughput is None):
        extraParameters.extend(['-target', str(targetThroughput)])
    localRunCommand = cluster.getRunCommand(pathForWorkloadFile, runtimeBenchmarkInMinutes, str(workloadThreads), extraParameters)
    executeCommandOnYcsbNodes(localRunCommand, localRunCommand, outputFile + '_ycsb_result', [])
    return pathRawInsertData, pathRawUpdateData

def plotResults(inputFile, outputFile):
    fileParser = FileParser()
    dataAboutConsistency = fileParser.parse(inputFile)
    dataAboutConsistency.removeWarmUpData(WARM_UP_TIME_IN_SECONDS)
    dataAboutConsistency.removeInvalidMeasurements()
    plotCdf(dataAboutConsistency, outputFile)