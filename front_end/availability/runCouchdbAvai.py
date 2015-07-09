#!/bin/python3

import sys

from availability.availabilityBenchmark import runAvailabilityBenchmark
from cluster.CouchdbCluster import CouchdbCluster

NORMAL_BINDING = 'couchdb'
CONSISTENCY_BINDING = 'couchdb_consistency'

def main():
    if len(sys.argv) < 8:
        printUsageAndExit()
    ipsInCluster=sys.argv[1]
    pathForWorkloadFile = sys.argv[2]
    pathBenchmarkResult = sys.argv[3]
    runtimeBenchmarkInMinutes = int(sys.argv[4])
    amountOfThreads = sys.argv[5]
    targetThroughput = sys.argv[6]
    eventFile = sys.argv[7]
    if targetThroughput == '-':
        targetThroughput = None
    if len(sys.argv) >= 9:
        remoteYcsbNodes = sys.argv[8].split(',')
    else:
        remoteYcsbNodes = []
    cluster = CouchdbCluster(NORMAL_BINDING, CONSISTENCY_BINDING, ipsInCluster)
    runAvailabilityBenchmark(cluster, remoteYcsbNodes, pathForWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, 
                             amountOfThreads, eventFile, targetThroughput)

def printUsageAndExit():
    print('usage: binary <ips in cluster> <path workload file> <path result file> <runtime benchmark (min)> <#threads> <throughput (ops/sec)/-> <eventFile> [<list remote ycsb nodes>]')
    exit()

main()