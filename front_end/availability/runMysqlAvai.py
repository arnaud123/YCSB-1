#!/bin/python3

import sys;

from availability.availabilityBenchmark import runAvailabilityBenchmark
from cluster import MySqlCluster

NORMAL_BINDING = 'jdbc';
CONSISTENCY_BINDING = 'jdbc_consistency';
IPS_IN_CLUSTER = ['172.16.33.11', '172.16.33.12', '172.16.33.13'];
IP_MASTER_NODE = '172.16.33.11';
PATH_TO_DB_PROPERTIES_FILE = '/root/YCSB/jdbc/db_properties';

def main():
    if len(sys.argv) < 7:
        printUsageAndExit(); 
    pathForWorkloadFile = sys.argv[1];
    pathBenchmarkResult = sys.argv[2];
    runtimeBenchmarkInMinutes = int(sys.argv[3]);
    amountOfThreads = sys.argv[4];
    targetThroughput = sys.argv[5];
    eventFile = sys.argv[6];
    if targetThroughput == '-':
        targetThroughput = None;
    if len(sys.argv) >= 8:
        remoteYcsbNodes = sys.argv[7].split(',');
    else:
        remoteYcsbNodes = [];
    cluster = MySqlCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER, IP_MASTER_NODE, PATH_TO_DB_PROPERTIES_FILE);
    cluster.writeDbPropertiesFile(remoteYcsbNodes);
    runAvailabilityBenchmark(cluster, remoteYcsbNodes, pathForWorkloadFile, pathBenchmarkResult, runtimeBenchmarkInMinutes, 
                             amountOfThreads, eventFile, targetThroughput);

def printUsageAndExit():
    print('usage: binary <path workload file> <path result file> <runtime benchmark (min)> <#threads> <throughput (ops/sec)/-> <eventFile> [<list remote ycsb nodes>]')
    exit();

main();