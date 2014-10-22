import sys;

from cluster.RiakCluster import RiakCluster;
from load.loadRoughScan.runRoughScan import runRoughScan

NORMAL_BINDING = 'riak';
CONSISTENCY_BINDING = 'riak_consistency';
IPS_IN_CLUSTER = ['172.16.33.14', '172.16.33.15', '172.16.33.16', '172.16.33.17', '172.16.33.18'];

def main():
    if len(sys.argv) < 5:
        printUsageAndExit();
    pathToWorkloadFile = sys.argv[1];
    pathBenchmarkResult = sys.argv[2];
    runtimeBenchmarkInMinutes = int(sys.argv[3]);
    listOfAmountOfThreads = sys.argv[4].split(',');
    cluster = RiakCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER);
    runRoughScan(cluster, pathToWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, listOfAmountOfThreads);

def printUsageAndExit():
    print('usage: binary <path workload file> <result dir> <runtime benchmark> <list of #threads>');
    exit();

main();