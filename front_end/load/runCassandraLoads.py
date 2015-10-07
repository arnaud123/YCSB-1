import sys;

from load.loadBenchmark import runLoadBenchmarkAsBatch;
from cluster.CassandraCluster import CassandraCluster;

NORMAL_BINDING = 'cassandra-10'
CONSISTENCY_BINDING = 'cassandra_consistency'
IPS_IN_CLUSTER = ['172.17.8.113', '172.17.8.114', '172.17.8.116', '172.17.8.115']

def main():
    if len(sys.argv) < 9:
        printUsageAndExit();
    pathToWorkloadFile = sys.argv[1]
    dirToWriteResultTo = sys.argv[2]
    runtimeBenchmarkInMinutes = int(sys.argv[3])
    writeConsistencyLevel = sys.argv[4]
    readConsistencyLevel = sys.argv[5]
    listOfOpsPerSec = sys.argv[6].split(',')
    listOfAmountThreads = sys.argv[7].split(',')
    listOfAmountOfMachines = sys.argv[8].split(',')
    if len(sys.argv) >= 10:
        remoteYcsbNodes = sys.argv[9].split(',')
    else:
        remoteYcsbNodes = []
    cluster = CassandraCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER,
                               readConsistencyLevel, writeConsistencyLevel)
    runLoadBenchmarkAsBatch(cluster, remoteYcsbNodes, pathToWorkloadFile, 
                        runtimeBenchmarkInMinutes, dirToWriteResultTo, 
                        listOfOpsPerSec, listOfAmountThreads, listOfAmountOfMachines)

def printUsageAndExit():
    print('usage: binary ' +
          '<path workload file> ' +
          '<result dir> ' +
          '<runtime benchmark> ' +
          '<write consistency level (ONE, QUORUM, ALL)> ' +
          '<read consistency level (ONE, QUORUM, ALL)> ' +
          '<list of #ops> ' +
          '<list of #threads> ' +
          '<list of #machines> ' +
          '[<list remote ycsb nodes>]')
    exit()

main()
