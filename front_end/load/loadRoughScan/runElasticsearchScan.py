import sys;

from cluster.ElasticsearchCluster import ElasticsearchCluster
from load.loadRoughScan.runRoughScan import runRoughScan

NORMAL_BINDING = 'elasticsearch'
CONSISTENCY_BINDING = 'elasticsearch'
IPS_IN_CLUSTER = ['172.16.8.166']

def main():
    if len(sys.argv) < 6:
        printUsageAndExit()
    pathToWorkloadFile = sys.argv[1]
    pathBenchmarkResult = sys.argv[2]
    runtimeBenchmarkInMinutes = int(sys.argv[3])
    clusterName = sys.argv[4]
    listOfAmountOfThreads = sys.argv[5].split(',')
    cluster = ElasticsearchCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER, clusterName)
    runRoughScan(cluster, pathToWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, listOfAmountOfThreads)

def printUsageAndExit():
    print('usage: binary ' +
          '<path workload file> ' +
          '<result dir> ' +
          '<runtime benchmark> ' +
          '<cluster name> ' +
          '<list of #threads>')
    exit()

main()
