import sys

from load.loadBenchmark import runLoadBenchmarkAsBatch
from cluster.MongoDbCluster import MongoDbCluster

NORMAL_BINDING = 'mongodb'
CONSISTENCY_BINDING = 'mongodb'
IPS_IN_CLUSTER = ['172.16.8.16', '172.16.8.17', '172.16.8.18', '172.16.8.19']
ACCESS_NODES = []

def main():
    if len(sys.argv) < 7:
        printUsageAndExit() 
    pathToWorkloadFile = sys.argv[1]
    dirToWriteResultTo = sys.argv[2]
    runtimeBenchmarkInMinutes = int(sys.argv[3])
    listOfOpsPerSec = sys.argv[4].split(',')
    listOfAmountThreads = sys.argv[5].split(',')
    listOfAmountOfMachines = sys.argv[6].split(',')
    if len(sys.argv) >= 8:
        remoteYcsbNodes = sys.argv[7].split(',')
    else:
        remoteYcsbNodes = []
    cluster = MongoDbCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER, ACCESS_NODES)
    runLoadBenchmarkAsBatch(cluster, remoteYcsbNodes, pathToWorkloadFile, 
                        runtimeBenchmarkInMinutes, dirToWriteResultTo, 
                        listOfOpsPerSec, listOfAmountThreads, listOfAmountOfMachines)

# TODO: Check mongodb driver specific properties

def printUsageAndExit():
    print('usage: binary <path workload file> <result dir> <runtime benchmark> <list of #ops> <list of #threads> <list of #machines> [<list remote ycsb nodes>]')
    exit()
    
main()