#!/bin/python3

import sys

from cluster.MongoDbCluster import MongoDbCluster
from availability.availabilityBenchmark import runAvailabilityBenchmark

NORMAL_BINDING = 'mongodb'
CONSISTENCY_BINDING = 'mongodb'

def main():
    if len(sys.argv) < 10:
        printUsageAndExit()
    ipsInCluster = sys.argv[1]
    readPreference = sys.argv[2]
    writeConcern = sys.argv[3]
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

    cluster = MongoDbCluster(NORMAL_BINDING, CONSISTENCY_BINDING, ipsInCluster,
                            ipsInCluster[0], writeConcern, readPreference)
    runAvailabilityBenchmark(cluster, remoteYcsbNodes, pathForWorkloadFile, pathBenchmarkResult,
                            runtimeBenchmarkInMinutes, amountOfThreads, eventFile, targetThroughput)

def printUsageAndExit():
    print('usage: binary <ips in cluster> <read preference (nearest, primary, primarypreferred, secondary, secondarypreferred)> <write concern (safe, journal, normal, fsync_safe, replicas_safe, majority)> <path workload file> <path result file> <runtime benchmark (min)> <#threads> <throughput (ops/sec)/-> <eventFile> [<list remote ycsb nodes>]')
    exit()

main()
