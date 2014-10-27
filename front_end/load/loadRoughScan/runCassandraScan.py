import sys;

from cluster.CassandraCluster import CassandraCluster;
from load.loadRoughScan.runRoughScan import runRoughScan

NORMAL_BINDING = 'cassandra-10';
CONSISTENCY_BINDING = 'cassandra_consistency';
IPS_IN_CLUSTER = ['172.16.8.16', '172.16.8.17', '172.16.8.18', '172.16.8.19'];

def main():
    if len(sys.argv) < 5:
        printUsageAndExit();
    pathToWorkloadFile = sys.argv[1];
    pathBenchmarkResult = sys.argv[2];
    runtimeBenchmarkInMinutes = int(sys.argv[3]);
    listOfAmountOfThreads = sys.argv[4].split(',');
    cluster = CassandraCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER);
    runRoughScan(cluster, pathToWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, listOfAmountOfThreads);

def printUsageAndExit():
    print('usage: binary <path workload file> <result dir> <runtime benchmark> <list of #threads>');
    exit();

main();
