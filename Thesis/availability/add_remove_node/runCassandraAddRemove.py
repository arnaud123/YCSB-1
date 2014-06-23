#!/bin/python

import sys;

from Thesis.availability.add_remove_node.addRemoveBenchmark import runAddRemoveBenchmark;
from Thesis.cluster.CassandraCluster import CassandraCluster;

NORMAL_BINDING = 'cassandra-10';
CONSISTENCY_BINDING = 'cassandra_consistency';
IPS_IN_CLUSTER = ['172.16.33.14', '172.16.33.15', '172.16.33.16', '172.16.33.17'];

def main():
    if len(sys.argv) < 9:
        printUsageAndExit(); 
    pathToWorkloadFile = sys.argv[1];
    pathBenchmarkResult = sys.argv[2];
    runtimeBenchmarkInMinutes = int(sys.argv[3]);
    removeTimeInSeconds = int(sys.argv[4])*60;
    addTimeInSeconds = int(sys.argv[5])*60;
    ipNodeToRemove = sys.argv[6];
    amountOfThreads = sys.argv[7];
    targetThroughput = sys.argv[8];
    if targetThroughput == '-':
        targetThroughput = None;
    if len(sys.argv) >= 10:
        remoteYcsbNodes = sys.argv[9].split(',');
    else:
        remoteYcsbNodes = [];
    cluster = CassandraCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER);
    runAddRemoveBenchmark(cluster, remoteYcsbNodes, ipNodeToRemove, pathToWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, 
                          removeTimeInSeconds, addTimeInSeconds, amountOfThreads, targetThroughput);

def printUsageAndExit():
    print 'usage: binary <path workload file> <path result file> <runtime benchmark (min)> <remove time (min)> <add time (min)> <ip remove node> <#threads> <throughput (ops/sec)/-> [<list remote ycsb nodes>]'
    exit();

main();