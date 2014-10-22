#!/bin/python3

import sys

from cluster.CassandraCluster import CassandraCluster
from consistency.consistencyBenchmark import runIncreasingLoadBenchmark

NORMAL_BINDING = 'cassandra-10'
CONSISTENCY_BINDING = 'cassandra_consistency'
IPS_IN_CLUSTER = ['172.16.33.14', '172.16.33.15', '172.16.33.16', '172.16.33.17']
DESTINATION_WORKLOAD_FILE = '/root/YCSB/workloads/workload_load'

def main():
    if len(sys.argv) < 13:
        printUsageAndExit()
    runtimeBenchmarkInMinutes = int(sys.argv[1])
    outputFile = sys.argv[2]
    readConsistencyLevel = sys.argv[3]
    writeConsistencyLevel = sys.argv[4]
    seedForOperationSelection = sys.argv[5]
    requestPeriod = int(sys.argv[6])
    accuracyInMicros = int(sys.argv[7])
    timeout = int(sys.argv[8])
    maxDelayBeforeDrop = int(sys.argv[9])
    stopOnFirstConsistency = (sys.argv[10].lower() == 'true')
    workloadThreads = int(sys.argv[11])
    listOfTargetThroughputs = sys.argv[12].strip('\n ').split(',')
    cassandraCluster = CassandraCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER)
    runIncreasingLoadBenchmark(cassandraCluster, runtimeBenchmarkInMinutes, DESTINATION_WORKLOAD_FILE, outputFile,
                               readConsistencyLevel, writeConsistencyLevel, seedForOperationSelection, requestPeriod,
                               accuracyInMicros, timeout, maxDelayBeforeDrop, stopOnFirstConsistency, workloadThreads,
                               listOfTargetThroughputs)

def printUsageAndExit():
    output = ['Usage: binary']
    output.append('<runtime benchmark (min)>')
    output.append('<output file>')
    output.append('<consistency level reads (ONE, QUORUM, ALL)>')
    output.append('<consistency level writes> (ONE, QUORUM, ALL)')
    output.append('<seed for operation selection>')
    output.append('<request period (millis)>')
    output.append('<accuracy (micros)>')
    output.append('<timeout (micros)>')
    output.append('<maxDelayBeforeDrop (micros) (<1 for unlimited)>')
    output.append('<stop first consistency (True/False)>')
    output.append('<#workload threads>')
    output.append('<list of target throughputs>')
    print(' '.join(output))
    exit()
    
main()