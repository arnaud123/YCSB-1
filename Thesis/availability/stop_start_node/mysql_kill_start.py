#!/bin/python

import sys;
import subprocess;

from time import sleep;
from threading import Thread;
from Thesis.ycsbClient.runMultipleYcsbClients import executeCommandOnYcsbNodes;
from Thesis.plot.ParseYcsbTestResults import parseAndPlot;
from Thesis.util.util import executeCommandOverSsh;

MYSQL_BINDING = "jdbc";
PATH_YCSB_EXECUTABLE = "/root/YCSB/bin/ycsb";
RECORD_COUNT = 1000;
OPERATION_COUNT = 999999999;
TIMESERIES_GRANULARITY = 2000;

def main():
    # Check amount input parameters
    if(len(sys.argv) != 9):
        printUsageAndExit('Illegal amount of input arguments');
    # Retrieve input parameters
    IpNodeToBeKilled = sys.argv[1];
    masterNodeIp = sys.argv[2];
    runtimeBenchmarkInSeconds = int(sys.argv[3])*60;
    killTimeInSeconds = float(sys.argv[4])*60;
    startTimeInSeconds = float(sys.argv[5])*60;
    pathToWorkloadFile = sys.argv[6];
    pathDbPropertiesFile = sys.argv[7];
    pathResultFile = sys.argv[8];
    # Check validity input parameters
    if(runtimeBenchmarkInSeconds <= 0 ):
        printUsageAndExit('Illegal runtime of benchmark argument');
    if(killTimeInSeconds < 0 or killTimeInSeconds > runtimeBenchmarkInSeconds):
        printUsageAndExit('Illegal kill at argument');
    if(startTimeInSeconds < 0 or startTimeInSeconds > runtimeBenchmarkInSeconds):
        printUsageAndExit('Illegal start at argument');
    # clear database
    executeCommandOverSsh(masterNodeIp, "mysql -u root -e 'use ycsb_database; delete from usertable;'");
    # Load database
    loadCommand = [PATH_YCSB_EXECUTABLE, 'load', MYSQL_BINDING];
    loadCommand.extend(['-P', pathToWorkloadFile]);
    loadCommand.extend(['-P', pathDbPropertiesFile]);
    loadCommand.extend(['-p', 'recordcount=' + str(RECORD_COUNT)]);
    loadCommand.extend(['-p', 'operationcount=' + str(OPERATION_COUNT)]);
    loadCommand.extend(['-p', 'measurementtype=timeseries']);
    loadCommand.extend(['-p', 'timeseries.granularity=' + str(TIMESERIES_GRANULARITY), '-s']);
    print "Loading database";
    exitCode = subprocess.call(loadCommand);
    if(exitCode != 0):
        raise Exception('Loading database failed');
    # Start benchmark
    runCommand = [PATH_YCSB_EXECUTABLE, 'run', MYSQL_BINDING]; 
    runCommand.extend(['-P', pathToWorkloadFile]);
    runCommand.extend(['-P', pathDbPropertiesFile]); 
    runCommand.extend(['-p', 'recordcount=' + str(RECORD_COUNT)]); 
    runCommand.extend(['-p', 'operationcount=' + str(OPERATION_COUNT)]); 
    runCommand.extend(['-p', 'measurementtype=timeseries']); 
    runCommand.extend(['-p', 'timeseries.granularity=' + str(TIMESERIES_GRANULARITY)]);
    runCommand.extend(['-p', 'maxexecutiontime=' + str(runtimeBenchmarkInSeconds), '-s']);
    print "Starting benchmark";
    benchmarkThread = Thread(target=executeCommandOnYcsbNodes, args=(runCommand, runCommand, pathResultFile, ['172.16.33.10']));
    benchmarkThread.start();
    # Stop node at "kill at"
    sleep(killTimeInSeconds);
    print "Stopping MySQL server at " + IpNodeToBeKilled;
    executeCommandOverSsh(IpNodeToBeKilled, "systemctl stop mysqld");
    # Start node at "start at"
    sleep(startTimeInSeconds - killTimeInSeconds);
    print "Starting MySQL server at " + IpNodeToBeKilled;
    executeCommandOverSsh(IpNodeToBeKilled, "systemctl start mysqld");
    # Wait for benchmark to finish and close result file
    benchmarkThread.join();
    # Plot results
    parseAndPlot(pathResultFile);

def printUsageAndExit(errorMessage):
    print 'Usage: script <IP node to be killed> <IP master node> <runtime of benchmark (min)> <kill at (min)> <start at (min)> <Path to workload file> <db properties file> <path result file>';
    exit();
    
main();