import sys;

from cluster.CassandraCluster import CassandraCluster;
from load.loadRoughScan.runRoughScan import runRoughScan

NORMAL_BINDING = 'cassandra-10'
CONSISTENCY_BINDING = 'cassandra_consistency'
IPS_IN_CLUSTER = ['172.17.8.70', '172.17.8.71', '172.17.8.72', '172.17.8.73', '172.17.8.68', '172.17.8.69']

def main():
    if len(sys.argv) < 7:
        printUsageAndExit()
    pathToWorkloadFile = sys.argv[1]
    pathBenchmarkResult = sys.argv[2]
    runtimeBenchmarkInMinutes = int(sys.argv[3])
    writeConsistencyLevel = sys.argv[4]
    readConsistencyLevel = sys.argv[5]
    listOfAmountOfThreads = sys.argv[6].split(',')
    cluster = CassandraCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER,
                               readConsistencyLevel, writeConsistencyLevel)
    runRoughScan(cluster, pathToWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, listOfAmountOfThreads)

def printUsageAndExit():
    print('usage: binary ' +
          '<path workload file> ' +
          '<result dir> ' +
          '<runtime benchmark> ' +
          '<write consistency level (ONE, QUORUM, ALL)> ' +
          '<read consistency level (ONE, QUORUM, ALL)> ' +
          '<list of #threads>')
    exit()

main()
