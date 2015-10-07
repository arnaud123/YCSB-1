import subprocess
import time

from util.util import checkExitCodeOfProcess
from consistency.processConsistencyResult.FileParser import FileParser
from consistency.processConsistencyResult.plotInconsistencyWindow import plotInconsistencyWindow
from ycsbClient.runMultipleYcsbClients import executeCommandOnYcsbNodes

WARM_UP_TIME_IN_SECONDS = 300

def runSingleLoadBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile, outputFile,
                           seedForOperationSelection, requestPeriod, accuracyInMicros, timeoutInMicros,
                           lastSamplepointInMicros, maxDelayBeforeDrop, stopOnFirstConsistency, workloadThreads,
                           targetThroughputWorkloadThreads):
    delayToWriteToResultFileMap = runBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile,
                                                          outputFile, seedForOperationSelection, requestPeriod,
                                                          accuracyInMicros, maxDelayBeforeDrop, stopOnFirstConsistency,
                                                          workloadThreads, lastSamplepointInMicros,
                                                          targetThroughputWorkloadThreads)
    delayToWriteToFilePathPairsForInsert, delayToWriteToFilePathPairsForUpdate = _composeDelayToWriteInMicrosToFilePathPairs(delayToWriteToResultFileMap)
    plotResults(delayToWriteToFilePathPairsForInsert, timeoutInMicros, outputFile + "_insert")
    plotResults(delayToWriteToFilePathPairsForUpdate, timeoutInMicros, outputFile + '_update')

def runIncreasingLoadBenchmark(cluster, runtimeBenchmarkInMinutes, pathForWorkloadFile, outputFile,
                               seedForOperationSelection, requestPeriod, accuracyInMicros, timeout, maxDelayBeforeDrop,
                               stopOnFirstConsistency, workloadThreads, listOfTargetThroughputs):
    rawDataPathsInsert = []
    rawDataPathsUpdate = []
    for targetThroughput in listOfTargetThroughputs:
        prepareDatabaseForBenchmark(cluster, pathForWorkloadFile)
        time.sleep(120)
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
                 stopOnFirstConsistency, workloadThreads, lastSamplepointInMicros, targetThroughput=None):
    resultFileMap = {}
    for i in range(0, lastSamplepointInMicros+1, accuracyInMicros):
        prepareDatabaseForBenchmark(cluster, pathToWorkloadFile)
        time.sleep(120)
        delayToWriteThread = 1 if i == 0 else i
        pathRawInsertData = outputFile + '_insertRawData_' + str(delayToWriteThread) + '_micros'
        pathRawUpdateData = outputFile + '_updateRawData_' + str(delayToWriteThread) + '_micros'
        pathConsistencyResult = outputFile + "_CONSISTENCY_RESULT_" + str(delayToWriteThread) + '_micros'
        extraParameters = []
        command = cluster.getConsistencyRunCommand(pathToWorkloadFile, pathConsistencyResult, runtimeBenchmarkInMinutes,
                                     workloadThreads, outputFile, requestPeriod, seedForOperationSelection,
                                     accuracyInMicros, maxDelayBeforeDrop, stopOnFirstConsistency, cluster,
                                     targetThroughput, pathRawInsertData, pathRawUpdateData, delayToWriteThread, extraParameters)
        executeCommandOnYcsbNodes(command, command, outputFile + '_ycsb_result_' + str(delayToWriteThread) + '_micros', [])
        resultFileMap[delayToWriteThread] = pathRawInsertData, pathRawUpdateData
    return resultFileMap

def plotResults(delayToWriteToFilePathPairs, timeoutInMicros, outputFile):
    parser = FileParser()
    consistencydataset = parser.parse(delayToWriteToFilePathPairs)
    consistencydataset.filterIllegalMeasurements(WARM_UP_TIME_IN_SECONDS*(10**6), timeoutInMicros)
    plotInconsistencyWindow(consistencydataset, outputFile)

def _composeDelayToWriteInMicrosToFilePathPairs(delayToWriteToResultFileMap):

    delayToWriteInMicrosToFilePathPairsForInsert = []
    delayToWriteInMicrosToFilePathPairsForUpdate = []
    for delayToWrite in sorted(delayToWriteToResultFileMap.keys()):
        pathRawInsertData, pathRawUpdateData = delayToWriteToResultFileMap[delayToWrite]
        delayToWriteInMicrosToFilePathPairsForInsert.append((delayToWrite, pathRawInsertData))
        delayToWriteInMicrosToFilePathPairsForUpdate.append((delayToWrite, pathRawUpdateData))
    return delayToWriteInMicrosToFilePathPairsForInsert, delayToWriteInMicrosToFilePathPairsForUpdate
