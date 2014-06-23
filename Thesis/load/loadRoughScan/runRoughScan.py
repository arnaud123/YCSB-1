import subprocess;

from Thesis.util.util import checkExitCodeOfProcess;
from Thesis.ycsbClient.runMultipleYcsbClients import executeCommandOnYcsbNodes;
from Thesis.plot.plotLoadRoughScan import writeLoadDataToCsv

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
    subprocess.call(['Rscript', '/root/YCSB/Thesis/plot/plot_load_rough_scan.r', plotDataFile, plotDataFile + '_graph.png']);

def loadDatabase(cluster, pathForWorkloadFile):
    loadCommand = cluster.getLoadCommand(pathForWorkloadFile);
    exitcode = subprocess.call(loadCommand);
    checkExitCodeOfProcess(exitcode, 'Loading database failed');
    
def runBenchmark(cluster, pathToWorkloadFile, runtimeBenchmarkInMinutes, pathBenchmarkResult, amountOfThreads):
    localRunCommand = cluster.getRunCommand(pathToWorkloadFile, runtimeBenchmarkInMinutes, amountOfThreads);
    executeCommandOnYcsbNodes(localRunCommand, localRunCommand, pathBenchmarkResult, []);