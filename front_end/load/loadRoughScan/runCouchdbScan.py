import sys;

from load.loadRoughScan.runRoughScan import runRoughScan
from cluster.CouchdbCluster import CouchdbCluster

NORMAL_BINDING = 'couchdb';
CONSISTENCY_BINDING = 'couchdb_consistency';
IPS_IN_CLUSTER = ['172.17.8.70', '172.17.8.68', '172.17.8.69', '172.17.8.71', '172.17.8.72', '172.17.8.73'];

def main():
    if len(sys.argv) < 5:
        printUsageAndExit();
    pathToWorkloadFile = sys.argv[1];
    pathBenchmarkResult = sys.argv[2];
    runtimeBenchmarkInMinutes = int(sys.argv[3]);
    listOfAmountOfThreads = sys.argv[4].split(',');
    cluster = CouchdbCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER);
    runRoughScan(cluster, pathToWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, listOfAmountOfThreads);

def printUsageAndExit():
    print('usage: binary <path workload file> <result dir> <runtime benchmark> <list of #threads>');
    exit();

main();
