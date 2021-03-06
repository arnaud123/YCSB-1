#!/bin/python

import sys;

from Thesis.cluster.CassandraCluster import CassandraCluster;
from Thesis.consistency.consistencyBenchmark import runIncreasingLoadBenchmark;

NORMAL_BINDING = 'cassandra-10';
CONSISTENCY_BINDING = 'cassandra_consistency';
IPS_IN_CLUSTER = ['172.16.33.14', '172.16.33.15', '172.16.33.16', '172.16.33.17'];
DESTINATION_WORKLOAD_FILE = '/root/YCSB/workloads/workload_load';

def main():
    if len(sys.argv) < 13:
        printUsageAndExit();
    runtimeBenchmarkInMinutes = int(sys.argv[1]);
    outputFile = sys.argv[2];
    readConsistencyLevel = sys.argv[3];
    writeConsistencyLevel = sys.argv[4];
    requestPeriod = int(sys.argv[5]);
    retryDelay = int(sys.argv[6]);
    timeout = int(sys.argv[7]);
    maxDelayBeforeDrop = int(sys.argv[8]);
    stopOnFirstConsistency = (sys.argv[9].lower() == 'true');
    amountOfReadThreads = int(sys.argv[10]);
    workloadThreads = int(sys.argv[11]);
    listOfTargetThroughputs = sys.argv[12].strip('\n ').split(',');
    cassandraCluster = CassandraCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER);
    runIncreasingLoadBenchmark(cassandraCluster, runtimeBenchmarkInMinutes, DESTINATION_WORKLOAD_FILE, outputFile, readConsistencyLevel, 
                               writeConsistencyLevel, requestPeriod, retryDelay, timeout, maxDelayBeforeDrop, 
                               stopOnFirstConsistency, amountOfReadThreads, workloadThreads, listOfTargetThroughputs)

def printUsageAndExit():
    output = ['Usage: binary'];
    output.append('<runtime benchmark (min)>');
    output.append('<output file>');
    output.append('<consistency level reads (ONE, QUORUM, ALL)>');
    output.append('<consistency level writes> (ONE, QUORUM, ALL)');
    output.append('<request period (millis)>');
    output.append('<retry delay (millis)>');
    output.append('<timeout (micros)>');
    output.append('<maxDelayBeforeDrop (micros) (<1 for unlimited)>');
    output.append('<stop first consistency (True/False)>');
    output.append('<#read threads>');
    output.append('<#workload threads>');
    output.append('<list of target throughputs>');
    print ' '.join(output);
    exit();
    
main();