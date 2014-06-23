#!/bin/python

import sys;

from Thesis.availability.stop_start_node.stopStartBenchmark import runStopStartBenchmark;
from Thesis.cluster.RiakCluster import RiakCluster;

NORMAL_BINDING = 'riak';
CONSISTENCY_BINDING = 'riak_consistency';
IPS_IN_CLUSTER = ['172.16.33.14', '172.16.33.15', '172.16.33.16', '172.16.33.17', '172.16.33.18'];

def main():
    if len(sys.argv) < 9:
        printUsageAndExit(); 
    pathForWorkloadFile = sys.argv[1];
    pathBenchmarkResult = sys.argv[2];
    runtimeBenchmarkInMinutes = int(sys.argv[3]);
    killTimeInSeconds = int(sys.argv[4])*60;
    startTimeInSeconds = int(sys.argv[5])*60;
    IpNodeToBeKilled = sys.argv[6];
    amountOfThreads = sys.argv[7];
    targetThroughput = sys.argv[8];
    if targetThroughput == '-':
        targetThroughput = None;
    if len(sys.argv) >= 10:
        remoteYcsbNodes = sys.argv[9].split(',');
    else:
        remoteYcsbNodes = [];
    cluster = RiakCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER);
    runStopStartBenchmark(cluster, remoteYcsbNodes, IpNodeToBeKilled, pathForWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, 
                          killTimeInSeconds, startTimeInSeconds, amountOfThreads, targetThroughput);

def printUsageAndExit():
    print 'usage: binary <path workload file> <path result file> <runtime benchmark (min)> <kill time (min)> <start time (min)> <ip kill node> <#threads> <throughput (ops/sec)/-> [<list remote ycsb nodes>]'
    exit();

main();