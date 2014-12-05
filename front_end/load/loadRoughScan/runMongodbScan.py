import sys;

from cluster.MongoDbCluster import MongoDbCluster
from load.loadRoughScan.runRoughScan import runRoughScan

NORMAL_BINDING = 'cassandra-10'
CONSISTENCY_BINDING = 'cassandra_consistency'
IPS_IN_CLUSTER = ['172.16.8.16', '172.16.8.17', '172.16.8.18', '172.16.8.19', '172.16.8.20', '172.16.8.21']
ACCESS_NODES = ['172.16.8.16']

def main():
    if len(sys.argv) < 7:
        printUsageAndExit()
    pathToWorkloadFile = sys.argv[1]
    pathBenchmarkResult = sys.argv[2]
    runtimeBenchmarkInMinutes = int(sys.argv[3])
    readPreference = sys.argv[4]
    writeConcern = sys.argv[5]
    listOfAmountOfThreads = sys.argv[6].split(',')
    cluster = MongoDbCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER, ACCESS_NODES,
                             writeConcern, readPreference)
    runRoughScan(cluster, pathToWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, listOfAmountOfThreads)

def printUsageAndExit():
    print('usage: binary ' +
          '<path workload file> ' +
          '<result dir> ' +
          '<runtime benchmark> ' +
          '<read preference (nearest, primary, primarypreferred, secondary, secondarypreferred)> ' +
          '<write concern (safe, journal, normal, fsync_safe, replicas_safe, majority)> ' +
          '<list of #threads>')
    exit()

main()
