import sys;

from cluster.MongoDbCluster import MongoDbCluster
from load.loadRoughScan.runRoughScan import runRoughScan

NORMAL_BINDING = 'mongodb'
CONSISTENCY_BINDING = 'mongodb'
IPS_IN_CLUSTER = ['172.17.8.106', '172.17.8.107', '172.17.8.105', '172.17.8.108']
ACCESS_NODES = ['172.17.8.106']

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
