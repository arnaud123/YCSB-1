#!/bin/python3

import sys

from consistency.consistencyBenchmark import runSingleLoadBenchmark
from cluster.CassandraCluster import CassandraCluster

NORMAL_BINDING = 'cassandra-10'
CONSISTENCY_BINDING = 'cassandra-10'
DESTINATION_WORKLOAD_FILE = 'workloads/workload_load'

def main():
    if len(sys.argv) < 15:
        printUsageAndExit()
    ipsInCluster = sys.argv[1]
    runtimeBenchmarkInMinutes = int(sys.argv[2])
    outputFile = sys.argv[3]
    readConsistencyLevel = sys.argv[4]
    writeConsistencyLevel = sys.argv[5]
    seedForOperationSelection = sys.argv[6]
    requestPeriod = int(sys.argv[7])
    accuracyInMicros = int(sys.argv[8])
    timeout = int(sys.argv[9])
    lastSamplePointInMicros = int(sys.argv[10])
    maxDelayBeforeDrop = int(sys.argv[11])
    stopOnFirstConsistency = (sys.argv[12].lower() == 'true')
    workloadThreads = int(sys.argv[13])
    targetThroughputWorkloadThreads = int(sys.argv[14])
    cassandraCluster = CassandraCluster(NORMAL_BINDING, CONSISTENCY_BINDING, ipsInCluster, readConsistencyLevel,
                                        writeConsistencyLevel)
    runSingleLoadBenchmark(cassandraCluster, runtimeBenchmarkInMinutes, DESTINATION_WORKLOAD_FILE, outputFile,
                           seedForOperationSelection, requestPeriod, accuracyInMicros, timeout, lastSamplePointInMicros,
                           maxDelayBeforeDrop, stopOnFirstConsistency, workloadThreads, targetThroughputWorkloadThreads)
    
def printUsageAndExit():
    output = ['Usage: binary']
    output.append('<ips in cluster>')
    output.append('<runtime benchmark (min)>')
    output.append('<output file>')
    output.append('<consistency level reads (ONE, QUORUM, ALL)>')
    output.append('<consistency level writes> (ONE, QUORUM, ALL)')
    output.append('<seed for operation selection>')
    output.append('<request period (millis)>')
    output.append('<accuracy (micros)>')
    output.append('<timeout (micros)>')
    output.append('<last samplepoint (micros)>')
    output.append('<maxDelayBeforeDrop (micros) (<1 for unlimited)>')
    output.append('<stop first consistency (True/False)>')
    output.append('<#workload threads>')
    output.append('<target throughput workload threads (ops/sec)>')
    print(' '.join(output))
    exit()
    
main()
