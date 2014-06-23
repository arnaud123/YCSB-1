#!/bin/python

import sys;

from time import sleep;
from threading import Thread;
from Thesis.ycsbClient.runMultipleYcsbClients import executeCommandOnYcsbNodes;
from Thesis.plot.ParseYcsbTestResults import parseAndPlot;
from Thesis.util.util import *;
from Thesis.delete_data.deleteAllCassandraData import clearCassandraColumnFamily;
from Thesis.util.ycsbCommands.Commands import getLoadCommand, getRunCommand

CASSANDRA_BINDING = "cassandra-10";
# PATH_YCSB_EXECUTABLE = "/root/YCSB/bin/ycsb";
# RECORD_COUNT = 1000;
# OPERATION_COUNT = 999999999;
# TIMESERIES_GRANULARITY = 2000;

def main():
    # Check amount input parameters
    if(len(sys.argv) != 7):
        printUsageAndExit('Illegal amount of input arguments');
    # Retrieve input parameters
    IpNodeToBeRemoved = sys.argv[1]; 
    runtimeBenchmarkInSeconds = int(sys.argv[2])*60;
    removeTimeInSeconds = float(sys.argv[3])*60;
    addTimeInSeconds = float(sys.argv[4])*60;
    pathToWorkloadFile = sys.argv[5];
    pathResultFile = sys.argv[6];
    # Check validity input parameters
    if(runtimeBenchmarkInSeconds <= 0 ):
        printUsageAndExit('Illegal runtime of benchmark argument');
    if(removeTimeInSeconds < 0 or removeTimeInSeconds > runtimeBenchmarkInSeconds):
        printUsageAndExit('Illegal remove at argument');
    if(addTimeInSeconds < 0 or addTimeInSeconds > runtimeBenchmarkInSeconds):
        printUsageAndExit('Illegal add at argument');
    # clear database
    clearCassandraColumnFamily(IpNodeToBeRemoved);
    # Load database
    loadCommand = getLoadCommand(CASSANDRA_BINDING, pathToWorkloadFile);
#     loadCommand = [PATH_YCSB_EXECUTABLE, 'load', CASSANDRA_BINDING];
#     loadCommand.extend(['-P', pathToWorkloadFile]);
#     loadCommand.extend(['-p', 'recordcount=' + str(RECORD_COUNT)]);
#     loadCommand.extend(['-p', 'operationcount=' + str(OPERATION_COUNT)]);
#     loadCommand.extend(['-p', 'measurementtype=timeseries']);
#     loadCommand.extend(['-p', 'timeseries.granularity=' + str(TIMESERIES_GRANULARITY), '-s']);    
    print "Loading database";
    exitCode = subprocess.call(loadCommand);
    if(exitCode != 0):
        raise Exception('Loading database failed');
    # Start benchmark
    runCommand = getRunCommand(CASSANDRA_BINDING, pathToWorkloadFile, runtimeBenchmarkInSeconds);
#     runCommand = [PATH_YCSB_EXECUTABLE, 'run', CASSANDRA_BINDING]; 
#     runCommand.extend(['-P', pathToWorkloadFile]); 
#     runCommand.extend(['-p', 'recordcount=' + str(RECORD_COUNT)]); 
#     runCommand.extend(['-p', 'operationcount=' + str(OPERATION_COUNT)]); 
#     runCommand.extend(['-p', 'measurementtype=timeseries']); 
#     runCommand.extend(['-p', 'timeseries.granularity=' + str(TIMESERIES_GRANULARITY)]);
#     runCommand.extend(['-p', 'maxexecutiontime=' + str(runtimeBenchmarkInSeconds), '-s']);
    print "Starting benchmark";
    benchmarkThread = Thread(target=executeCommandOnYcsbNodes, args=(runCommand, runCommand, pathResultFile, ['172.16.33.10']));
    benchmarkThread.start();
    # Stop node at "kill at"
    sleep(removeTimeInSeconds);
    print "Removing Cassandra node from cluster: " + IpNodeToBeRemoved;
    decommissionProcess = subprocess.Popen(["ssh", "root@" + IpNodeToBeRemoved, "nodetool decommission"]);
    # Start node at "start at"
    sleep(addTimeInSeconds - removeTimeInSeconds);
    print "Adding Cassandra node to cluster:  " + IpNodeToBeRemoved;
    executeCommandOverSsh(IpNodeToBeRemoved, "systemctl stop cassandra; rm -rf /var/lib/cassandra/commitlog/*; rm -rf /var/lib/cassandra/data/*; rm -rf /var/lib/cassandra/saved_caches/*; systemctl start cassandra");
    # Wait for benchmark to finish and close result file
    benchmarkThread.join();
    decommissionProcess.communicate();
    checkExitCodeOfProcess(decommissionProcess.poll(), 'Decommission process failed');
    # Plot results
    parseAndPlot(pathResultFile);

def printUsageAndExit(errorMessage):
    print 'Usage: script <IP node to be removed> <runtime of benchmark (min)> <remove at (min)> <add at (min)> <Path to workload file> <Path result file>';
    exit();
    
main();