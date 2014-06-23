#!/bin/python

import sys;

from Thesis.availability.add_remove_node.addRemoveBenchmark import runAddRemoveBenchmark;
from Thesis.cluster.MySqlCluster import MySqlCluster;

NORMAL_BINDING = 'jdbc';
CONSISTENCY_BINDING = 'jdbc_consistency';
IPS_IN_CLUSTER = ['172.16.33.11', '172.16.33.12', '172.16.33.13'];
IP_MASTER_NODE = '172.16.33.11';
PATH_TO_DB_PROPERTIES_FILE = '/root/YCSB/jdbc/db_properties';

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
    cluster = MySqlCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER, IP_MASTER_NODE, PATH_TO_DB_PROPERTIES_FILE);
    cluster.writeDbPropertiesFile(remoteYcsbNodes);
    runAddRemoveBenchmark(cluster, remoteYcsbNodes, ipNodeToRemove, pathToWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, 
                          removeTimeInSeconds, addTimeInSeconds, amountOfThreads, targetThroughput);

def printUsageAndExit():
    print 'usage: binary <path workload file> <path result file> <runtime benchmark (min)> <remove time (min)> <add time (min)> <ip remove node> <#threads> <throughput (ops/sec)/-> [<list remote ycsb nodes>]'
    exit();

main();