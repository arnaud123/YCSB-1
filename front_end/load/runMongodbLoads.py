import sys

from load.loadBenchmark import runLoadBenchmarkAsBatch
from cluster.MongoDbCluster import MongoDbCluster

NORMAL_BINDING = 'mongodb'
CONSISTENCY_BINDING = 'mongodb'
IPS_IN_CLUSTER = ['172.16.8.16', '172.16.8.17', '172.16.8.18', '172.16.8.19']
ACCESS_NODES = []

def main():
    if len(sys.argv) < 9:
        printUsageAndExit() 
    pathToWorkloadFile = sys.argv[1]
    dirToWriteResultTo = sys.argv[2]
    runtimeBenchmarkInMinutes = int(sys.argv[3])
    readPreference = sys.argv[4]
    writeConcern = sys.argv[5]
    listOfOpsPerSec = sys.argv[6].split(',')
    listOfAmountThreads = sys.argv[7].split(',')
    listOfAmountOfMachines = sys.argv[8].split(',')
    if len(sys.argv) >= 10:
        remoteYcsbNodes = sys.argv[9].split(',')
    else:
        remoteYcsbNodes = []
    cluster = MongoDbCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER, ACCESS_NODES,
                             writeConcern, readPreference)
    runLoadBenchmarkAsBatch(cluster, remoteYcsbNodes, pathToWorkloadFile, 
                        runtimeBenchmarkInMinutes, dirToWriteResultTo, 
                        listOfOpsPerSec, listOfAmountThreads, listOfAmountOfMachines)

def printUsageAndExit():
    print('usage: binary ' +
          '<path workload file> ' +
          '<result dir> ' +
          '<runtime benchmark> ' +
          '<read preference (nearest, primary, primarypreferred, secondary, secondarypreferred)> ' +
          '<write concern (safe, journal, normal, fsync_safe, replicas_safe, majority)> ' +
          '<list of #ops> ' +
          '<list of #threads> ' +
          '<list of #machines> ' +
          '[<list remote ycsb nodes>]')
    exit()
    
main()