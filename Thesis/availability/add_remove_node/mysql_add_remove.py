#!/bin/python

import sys;
import subprocess;

from time import sleep;
from threading import Thread;
from Thesis.ycsbClient.runMultipleYcsbClients import executeCommandOnYcsbNodes;
from Thesis.plot.ParseYcsbTestResults import parseAndPlot;
from Thesis.util.util import executeCommandOverSsh;
from Thesis.util.ycsbCommands.Commands import getLoadCommand;
from Thesis.util.ycsbCommands.Commands import getRunCommand;

MYSQL_BINDING = "jdbc";
# PATH_YCSB_EXECUTABLE = "/root/YCSB/bin/ycsb";
# RECORD_COUNT = 1000;
# OPERATION_COUNT = 999999999;
# TIMESERIES_GRANULARITY = 2000;

def main():
    # Check amount input parameters
    if(len(sys.argv) != 9):
        printUsageAndExit('Illegal amount of input arguments');
    # Retrieve input parameters
    IpNodeToBeRemoved = sys.argv[1];
    masterNodeIp = sys.argv[2];
    runtimeBenchmarkInSeconds = int(sys.argv[3])*60;
    removeTimeInSeconds = float(sys.argv[4])*60;
    addTimeInSeconds = float(sys.argv[5])*60;
    pathToWorkloadFile = sys.argv[6];
    pathDbPropertiesFile = sys.argv[7];
    pathResultFile = sys.argv[8];
    # Check validity input parameters
    if(runtimeBenchmarkInSeconds <= 0 ):
        printUsageAndExit('Illegal runtime of benchmark argument');
    if(removeTimeInSeconds < 0 or removeTimeInSeconds > runtimeBenchmarkInSeconds):
        printUsageAndExit('Illegal remove at argument');
    if(addTimeInSeconds < 0 or addTimeInSeconds > runtimeBenchmarkInSeconds):
        printUsageAndExit('Illegal add at argument');
    # clear database
    executeCommandOverSsh(masterNodeIp, "mysql -u root -e 'use ycsb_database; delete from usertable;'");
    # Load database
    loadCommand = getLoadCommand(MYSQL_BINDING, pathToWorkloadFile, ['-P', pathDbPropertiesFile]);
#     loadCommand = [PATH_YCSB_EXECUTABLE, 'load', MYSQL_BINDING];
#     loadCommand.extend(['-P', pathToWorkloadFile]);
#     loadCommand.extend(['-P', pathDbPropertiesFile]);
#     loadCommand.extend(['-p', 'recordcount=' + str(RECORD_COUNT)]);
#     loadCommand.extend(['-p', 'operationcount=' + str(OPERATION_COUNT)]);
#     loadCommand.extend(['-p', 'measurementtype=timeseries']);
#     loadCommand.extend(['-p', 'timeseries.granularity=' + str(TIMESERIES_GRANULARITY), '-s']);
    print "Loading database";
    exitCode = subprocess.call(loadCommand);
    if(exitCode != 0):
        raise Exception('Loading database failed');
    # Start benchmark
    runCommand= getRunCommand(MYSQL_BINDING, pathToWorkloadFile, runtimeBenchmarkInSeconds, ['-P', pathDbPropertiesFile]);
#     runCommand = [PATH_YCSB_EXECUTABLE, 'run', MYSQL_BINDING]; 
#     runCommand.extend(['-P', pathToWorkloadFile]);
#     runCommand.extend(['-P', pathDbPropertiesFile]); 
#     runCommand.extend(['-p', 'recordcount=' + str(RECORD_COUNT)]); 
#     runCommand.extend(['-p', 'operationcount=' + str(OPERATION_COUNT)]); 
#     runCommand.extend(['-p', 'measurementtype=timeseries']); 
#     runCommand.extend(['-p', 'timeseries.granularity=' + str(TIMESERIES_GRANULARITY)]);
#     runCommand.extend(['-p', 'maxexecutiontime=' + str(runtimeBenchmarkInSeconds), '-s']);
    print "Starting benchmark";
    benchmarkThread = Thread(target=executeCommandOnYcsbNodes, args=(runCommand, runCommand, pathResultFile, ['172.16.33.10']));
    benchmarkThread.start();
    # remove node at "remove at"
    sleep(removeTimeInSeconds);
    print "Removing MySQL node: " + IpNodeToBeRemoved;
    executeCommandOverSsh(IpNodeToBeRemoved, "mysql -u root -e 'slave stop'");
    # add node at "add at"
    sleep(addTimeInSeconds - removeTimeInSeconds);
    print "Adding MySQL node: " + IpNodeToBeRemoved;
    executeCommandOverSsh(IpNodeToBeRemoved, "mysql -u root -e 'slave start'");
    # Wait for benchmark to finish and close result file
    benchmarkThread.join();
    # Plot results
    parseAndPlot(pathResultFile);

def printUsageAndExit(errorMessage):
    print 'Usage: script <IP node to be removed> <IP master node> <runtime of benchmark (min)> <remove at (min)> <add at (min)> <Path to workload file> <db properties file> <path result file>';
    exit();
    
main();