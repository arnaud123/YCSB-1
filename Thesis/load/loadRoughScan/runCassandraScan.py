import sys;

from Thesis.cluster.CassandraCluster import CassandraCluster;
from Thesis.load.loadRoughScan.runRoughScan import runRoughScan

NORMAL_BINDING = 'cassandra-10';
CONSISTENCY_BINDING = 'cassandra_consistency';
IPS_IN_CLUSTER = ['172.16.33.14', '172.16.33.15', '172.16.33.16', '172.16.33.17'];

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
    print 'usage: binary <path workload file> <result dir> <runtime benchmark> <list of #threads>';
    exit();

main();