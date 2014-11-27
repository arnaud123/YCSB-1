#!/bin/python3

import sys

from consistency.consistencyBenchmark import runSingleLoadBenchmark
from cluster.MongoDbCluster import MongoDbCluster

NORMAL_BINDING = 'mongodb'
CONSISTENCY_BINDING = 'mongodb'
IPS_IN_CLUSTER = ['172.16.8.16', '172.16.8.17', '172.16.8.18', '172.16.8.19', '172.16.8.20', '172.16.8.21']
ACCESS_NODES = ['172.16.8.16']
DESTINATION_WORKLOAD_FILE = 'workloads/workload_load'

def main():
    if len(sys.argv) < 14:
        printUsageAndExit()
    runtimeBenchmarkInMinutes = int(sys.argv[1])
    outputFile = sys.argv[2]
    readPreference = sys.argv[3]
    writeConcern = sys.argv[4]
    seedForOperationSelection = sys.argv[5]
    requestPeriod = int(sys.argv[6])
    accuracyInMicros = int(sys.argv[7])
    timeout = int(sys.argv[8])
    lastSamplePointInMicros = int(sys.argv[9])
    maxDelayBeforeDrop = int(sys.argv[10])
    stopOnFirstConsistency = (sys.argv[11].lower() == 'true')
    workloadThreads = int(sys.argv[12])
    targetThroughputWorkloadThreads = int(sys.argv[13])
    mongodbCluster = MongoDbCluster(NORMAL_BINDING, CONSISTENCY_BINDING, IPS_IN_CLUSTER, ACCESS_NODES,
                                    writeConcern, readPreference)
    runSingleLoadBenchmark(mongodbCluster, runtimeBenchmarkInMinutes, DESTINATION_WORKLOAD_FILE, outputFile,
                           seedForOperationSelection, requestPeriod, accuracyInMicros, timeout, lastSamplePointInMicros,
                           maxDelayBeforeDrop, stopOnFirstConsistency, workloadThreads, targetThroughputWorkloadThreads)

def printUsageAndExit():
    output = ['Usage: binary']
    output.append('<runtime benchmark (min)>')
    output.append('<output file>')
    output.append('<read preference (nearest, primary, primarypreferred, secondary, secondarypreferred)>')
    output.append('<write concern> (safe, normal, fsync_safe, replicas_safe, majority)')
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
