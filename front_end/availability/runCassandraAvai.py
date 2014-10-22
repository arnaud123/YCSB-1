#!/bin/python

import sys;

from cluster.CassandraCluster import CassandraCluster;
from availability.availabilityBenchmark import runAvailabilityBenchmark

NORMAL_BINDING = 'cassandra-10';
CONSISTENCY_BINDING = 'cassandra_consistency';
IPS_IN_CLUSTER = ['172.16.33.14', '172.16.33.15', '172.16.33.16', '172.16.33.17'];

def main():
    if len(sys.argv) < 7:
        printUsageAndExit(); 
    pathForWorkloadFile = sys.argv[1];
    pathBenchmarkResult = sys.argv[2];
    runtimeBenchmarkInMinutes = int(sys.argv[3]);
    amountOfThreads = sys.argv[4];
    targetThroughput = sys.argv[5];
    eventFile = sys.argv[6]
    if targetThroughput == '-':
        targetThroughput = None;
    if len(sys.argv) >= 8:
        remoteYcsbNodes = sys.argv[7].split(',');
    else:
        remoteYcsbNodes = [];
    cluster = CassandraCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER);
    runAvailabilityBenchmark(cluster, remoteYcsbNodes, pathForWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, 
                            amountOfThreads, eventFile, targetThroughput);

def printUsageAndExit():
    print('usage: binary <path workload file> <path result file> <runtime benchmark (min)> <#threads> <throughput (ops/sec)/-> <eventFile> [<list remote ycsb nodes>]')
    exit();

main();