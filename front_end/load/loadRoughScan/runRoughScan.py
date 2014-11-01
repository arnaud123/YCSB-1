import subprocess;

from util.util import checkExitCodeOfProcess;
from ycsbClient.runMultipleYcsbClients import executeCommandOnYcsbNodes;
from plot.plotLoadRoughScan import writeLoadDataToCsv

ROUGH_SCAN_PLOT_SCRIPT = 'front_end/plot/plot_load_rough_scan.r'

def runRoughScan(cluster, pathToWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, 
                          listOfAmountOfThreads):
    resultFiles = [];
    for amountOfThreads in listOfAmountOfThreads:
        # Clear database
        cluster.deleteDataInCluster();
        cluster.writeNormalWorkloadFile([], pathToWorkloadFile);
        # Load database
        loadDatabase(cluster, pathToWorkloadFile); 
        # Start benchmark
        resultFile = pathBenchmarkResult + '_' + amountOfThreads;
        runBenchmark(cluster, pathToWorkloadFile, runtimeBenchmarkInMinutes, resultFile, amountOfThreads);
        resultFiles.append(resultFile);
    plotDataFile = pathBenchmarkResult + '_result'
    writeLoadDataToCsv(resultFiles, plotDataFile);
    subprocess.call(['Rscript', ROUGH_SCAN_PLOT_SCRIPT, plotDataFile, plotDataFile + '_graph.png']);

def loadDatabase(cluster, pathForWorkloadFile):
    loadCommand = cluster.getLoadCommand(pathForWorkloadFile);
    exitcode = subprocess.call(loadCommand);
    checkExitCodeOfProcess(exitcode, 'Loading database failed');
    
def runBenchmark(cluster, pathToWorkloadFile, runtimeBenchmarkInMinutes, pathBenchmarkResult, amountOfThreads):
    localRunCommand = cluster.getRunCommand(pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads);
    executeCommandOnYcsbNodes(localRunCommand, localRunCommand, pathBenchmarkResult, []);