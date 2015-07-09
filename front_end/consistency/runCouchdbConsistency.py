#!/bin/python3

import sys

from consistency.consistencyBenchmark import runSingleLoadBenchmark
from cluster.CouchdbCluster import CouchdbCluster

NORMAL_BINDING = 'couchdb'
CONSISTENCY_BINDING = 'couchdb'
DESTINATION_WORKLOAD_FILE = 'workloads/workload_load'

def main():
    if len(sys.argv) < 13:
        printUsageAndExit()
    ipsInCluster = sys.argv[1]
    runtimeBenchmarkInMinutes = int(sys.argv[2])
    outputFile = sys.argv[3]
    seedForOperationSelection = sys.argv[4]
    requestPeriod = int(sys.argv[5])
    accuracyInMicros = int(sys.argv[6])
    timeout = int(sys.argv[7])
    lastSamplepointInMicros = int(sys.argv[8])
    maxDelayBeforeDrop = int(sys.argv[9])
    stopOnFirstConsistency = (sys.argv[10].lower() == 'true')
    workloadThreads = int(sys.argv[11])
    targetThroughputWorkloadThreads = int(sys.argv[12])
    couchdbCluster = CouchdbCluster(NORMAL_BINDING, CONSISTENCY_BINDING, ipsInCluster)
    runSingleLoadBenchmark(couchdbCluster, runtimeBenchmarkInMinutes, DESTINATION_WORKLOAD_FILE, outputFile,
                           seedForOperationSelection, requestPeriod, accuracyInMicros, timeout, lastSamplepointInMicros,
                           maxDelayBeforeDrop, stopOnFirstConsistency, workloadThreads, targetThroughputWorkloadThreads)
    
def printUsageAndExit():
    output = ['Usage: binary']
    output.append('<ips in cluster>')
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
