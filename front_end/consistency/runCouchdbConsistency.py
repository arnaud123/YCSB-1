#!/bin/python3

import sys

from consistency.consistencyBenchmark import runSingleLoadBenchmark
from cluster.CouchdbCluster import CouchdbCluster

NORMAL_BINDING = 'couchdb'
CONSISTENCY_BINDING = 'couchdb'
IPS_IN_CLUSTER = ['172.16.8.16', '172.16.8.17', '172.16.8.18']
DESTINATION_WORKLOAD_FILE = 'workloads/workload_load'

def main():
    if len(sys.argv) < 12:
        printUsageAndExit()
    runtimeBenchmarkInMinutes = int(sys.argv[1])
    outputFile = sys.argv[2]
    seedForOperationSelection = sys.argv[3]
    requestPeriod = int(sys.argv[4])
    accuracyInMicros = int(sys.argv[5])
    timeout = int(sys.argv[6])
    lastSamplepointInMicros = int(sys.argv[7])
    maxDelayBeforeDrop = int(sys.argv[8])
    stopOnFirstConsistency = (sys.argv[9].lower() == 'true')
    workloadThreads = int(sys.argv[10])
    targetThroughputWorkloadThreads = int(sys.argv[11])
    couchdbCluster = CouchdbCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER)
    runSingleLoadBenchmark(couchdbCluster, runtimeBenchmarkInMinutes, DESTINATION_WORKLOAD_FILE, outputFile,
                           seedForOperationSelection, requestPeriod, accuracyInMicros, timeout, lastSamplepointInMicros,
                           maxDelayBeforeDrop, stopOnFirstConsistency, workloadThreads, targetThroughputWorkloadThreads)
    
def printUsageAndExit():
    output = ['Usage: binary']
    output.append('<runtime benchmark (min)>')
    output.append('<output file>')
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
