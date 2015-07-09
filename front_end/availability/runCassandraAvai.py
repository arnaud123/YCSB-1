#!/bin/python3

import sys

from cluster.CassandraCluster import CassandraCluster
from availability.availabilityBenchmark import runAvailabilityBenchmark

NORMAL_BINDING = 'cassandra-10'
CONSISTENCY_BINDING = 'cassandra_consistency'

def main():
    if len(sys.argv) < 10:
        printUsageAndExit()
    ipsInCluster = sys.argv[1]
    readConsistencyLevel = sys.argv[2]
    writeConsistencyLevel = sys.argv[3]
    pathForWorkloadFile = sys.argv[4]
    pathBenchmarkResult = sys.argv[5]
    runtimeBenchmarkInMinutes = int(sys.argv[6])
    amountOfThreads = sys.argv[7]
    targetThroughput = sys.argv[8]
    eventFile = sys.argv[9]
    if targetThroughput == '-':
        targetThroughput = None
    if len(sys.argv) >= 11:
        remoteYcsbNodes = sys.argv[10].split(',')
    else:
        remoteYcsbNodes = []
    cluster = CassandraCluster(NORMAL_BINDING, CONSISTENCY_BINDING, ipsInCluster, readConsistencyLevel, writeConsistencyLevel)
    runAvailabilityBenchmark(cluster, remoteYcsbNodes, pathForWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, 
                            amountOfThreads, eventFile, targetThroughput)

def printUsageAndExit():
    print('usage: binary <ips in cluster> <read consistency level (ONE, QUORUM, ALL)> <write consistency level (ONE, QUORUM, ALL)> <path workload file> <path result file> <runtime benchmark (min)> <#threads> <throughput (ops/sec)/-> <eventFile> [<list remote ycsb nodes>]')
    exit()

main()