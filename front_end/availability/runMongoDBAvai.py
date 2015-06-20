#!/bin/python3

import sys

from cluster.MongoDbCluster import MongoDbCluster
from availability.availabilityBenchmark import runAvailabilityBenchmark

NORMAL_BINDING = 'mongodb'
CONSISTENCY_BINDING = 'mongodb'
IPS_IN_CLUSTER = ['172.16.8.170', '172.16.8.171', '172.16.8.173', '172.16.8.174', '172.16.8.175']
ACCESS_NODES = ['172.16.8.170']
WRITE_CONCERN = 'journal'
READ_PREFERENCE = 'primary'

def main():
    if len(sys.argv) < 7:
        printUsageAndExit()
    pathForWorkloadFile = sys.argv[1]
    pathBenchmarkResult = sys.argv[2]
    runtimeBenchmarkInMinutes = int(sys.argv[3])
    amountOfThreads = sys.argv[4]
    targetThroughput = sys.argv[5]
    eventFile = sys.argv[6]
    if targetThroughput == '-':
        targetThroughput = None
    if len(sys.argv) >= 8:
        remoteYcsbNodes = sys.argv[7].split(',')
    else:
        remoteYcsbNodes = []

    cluster = MongoDbCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER,
                            ACCESS_NODES, WRITE_CONCERN, READ_PREFERENCE)
    runAvailabilityBenchmark(cluster, remoteYcsbNodes, pathForWorkloadFile, pathBenchmarkResult,
                            runtimeBenchmarkInMinutes, amountOfThreads, eventFile, targetThroughput)

def printUsageAndExit():
    print('usage: binary <path workload file> <path result file> <runtime benchmark (min)> <#threads> <throughput (ops/sec)/-> <eventFile> [<list remote ycsb nodes>]')
    exit()

main()