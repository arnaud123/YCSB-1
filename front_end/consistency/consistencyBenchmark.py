import subprocess

from util.util import checkExitCodeOfProcess
from consistency.processConsistencyResult.FileParser import FileParser
from consistency.processConsistencyResult.plotCdf import plotCdf
from ycsbClient.runMultipleYcsbClients import executeCommandOnYcsbNodes

WARM_UP_TIME_IN_SECONDS = 120

def runSingleLoadBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile, outputFile,
                           seedForOperationSelection, requestPeriod, accuracyInMicros, timeout, maxDelayBeforeDrop,
                           stopOnFirstConsistency, workloadThreads, targetThroughputWorkloadThreads):
    prepareDatabaseForBenchmark(cluster, pathForWorkloadFile)
    resultFileMap = runBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile,
                                                          outputFile, seedForOperationSelection, requestPeriod,
                                                          accuracyInMicros, maxDelayBeforeDrop, stopOnFirstConsistency,
                                                          workloadThreads, targetThroughputWorkloadThreads)
    # plotResults(pathRawInsertData, outputFile + '_insert', timeout, accuracyInMicros)
    # plotResults(pathRawUpdateData, outputFile + '_update', timeout, accuracyInMicros)

def runIncreasingLoadBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile, outputFile,
                               seedForOperationSelection, requestPeriod, accuracyInMicros, timeout, maxDelayBeforeDrop,
                               stopOnFirstConsistency, workloadThreads, listOfTargetThroughputs):
    rawDataPathsInsert = []
    rawDataPathsUpdate = []
    for targetThroughput in listOfTargetThroughputs:
        prepareDatabaseForBenchmark(cluster, pathForWorkloadFile)
        outputFileCurrentTest = outputFile + '_throughput_' + targetThroughput
        (pathRawInsertData, pathRawUpdateData) = runBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile,
                                                              outputFileCurrentTest, seedForOperationSelection,
                                                              requestPeriod, accuracyInMicros, maxDelayBeforeDrop,
                                                              stopOnFirstConsistency, workloadThreads,
                                                              int(targetThroughput))
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

def runBenchmark(cluster, runtimeBenchmarkInMinutes, pathToWorkloadFile, outputFile,
                 seedForOperationSelection, requestPeriod, accuracyInMicros, maxDelayBeforeDrop,
                 stopOnFirstConsistency, workloadThreads, targetThroughput=None):
    resultFileMap = {}
    for i in range(1,requestPeriod*1000, accuracyInMicros):
        pathRawInsertData = outputFile + '_insertRawData' + str(i) + 'micros'
        pathRawUpdateData = outputFile + '_updateRawData' + str(i) + 'micros'
        pathConsistencyResult = outputFile + "_CONSISTENCY_RESULT" + str(i) + 'micros'
        extraParameters = []
        command = cluster.getConsistencyRunCommand(pathToWorkloadFile, pathConsistencyResult, runtimeBenchmarkInMinutes,
                                     workloadThreads, outputFile, requestPeriod, seedForOperationSelection,
                                     accuracyInMicros, maxDelayBeforeDrop, stopOnFirstConsistency, cluster,
                                     targetThroughput, pathRawInsertData, pathRawUpdateData, extraParameters)
        executeCommandOnYcsbNodes(command, command, outputFile + '_ycsb_result' + str(i) + 'micros', [])
        resultFileMap[i] = pathRawInsertData, pathRawUpdateData
    return resultFileMap

def plotResults(inputFile, outputFile, timeoutInMicros, accuracyInMicros):
    fileParser = FileParser()
    dataAboutConsistency = fileParser.parse(inputFile, timeoutInMicros, accuracyInMicros)
    dataAboutConsistency.removeWarmUpData(WARM_UP_TIME_IN_SECONDS)
    dataAboutConsistency.removeInvalidMeasurements()
    plotCdf(dataAboutConsistency, outputFile)