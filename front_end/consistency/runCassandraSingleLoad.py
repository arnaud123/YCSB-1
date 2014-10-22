#!/bin/python3

import sys

from consistency.consistencyBenchmark import runSingleLoadBenchmark
from cluster.CassandraCluster import CassandraCluster

NORMAL_BINDING = 'cassandra-10'
CONSISTENCY_BINDING = 'cassandra_consistency'
IPS_IN_CLUSTER = ['172.16.8.16', '172.16.8.17']
DESTINATION_WORKLOAD_FILE = '/root/YCSB/workloads/workload_load'

def main():
    if len(sys.argv) < 11:
        printUsageAndExit()
    runtimeBenchmarkInMinutes = int(sys.argv[1])
    outputFile = sys.argv[2]
    readConsistencyLevel = sys.argv[3]
    writeConsistencyLevel = sys.argv[4]
    seedForOperationSelection = sys.argv[5]
    requestPeriod = int(sys.argv[6])
    timeout = int(sys.argv[7])
    maxDelayBeforeDrop = int(sys.argv[8])
    stopOnFirstConsistency = (sys.argv[9].lower() == 'true')
    workloadThreads = int(sys.argv[10])
    cassandraCluster = CassandraCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER)
    runSingleLoadBenchmark(cassandraCluster, runtimeBenchmarkInMinutes, DESTINATION_WORKLOAD_FILE, outputFile,
                           readConsistencyLevel, writeConsistencyLevel, seedForOperationSelection, requestPeriod,
                           timeout, maxDelayBeforeDrop, stopOnFirstConsistency, workloadThreads)
    
def printUsageAndExit():
    output = ['Usage: binary']
    output.append('<runtime benchmark (min)>')
    output.append('<output file>')
    output.append('<consistency level reads (ONE, QUORUM, ALL)>')
    output.append('<consistency level writes> (ONE, QUORUM, ALL)')
    output.append('<seed for operation selection>')
    output.append('<request period (millis)>')
    output.append('<timeout (micros)>')
    output.append('<maxDelayBeforeDrop (micros) (<1 for unlimited)>')
    output.append('<stop first consistency (True/False)>')
    output.append('<#workload threads>')
    print(' '.join(output))
    exit()
    
main()
