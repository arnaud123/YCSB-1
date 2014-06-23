#!/bin/python

import sys;
import subprocess;

from time import sleep;
from threading import Thread;
from Thesis.ycsbClient.runMultipleYcsbClients import executeCommandOnYcsbNodes;
from Thesis.plot.ParseYcsbTestResults import parseAndPlot;
from Thesis.delete_data.deleteAllRiakData import deleteAllDataInRiak;
from Thesis.util.util import executeCommandOverSsh;
from Thesis.util.ycsbCommands.Commands import getLoadCommand;
from Thesis.util.ycsbCommands.Commands import getRunCommand;

RIAK_BINDING = "riak";
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
    seedIp = sys.argv[2];
    ipsInCluster = sys.argv[3].split(',');
    runtimeBenchmarkInSeconds = int(sys.argv[4])*60;
    removeTimeInSeconds = float(sys.argv[5])*60;
    addTimeInSeconds = float(sys.argv[6])*60;
    pathToWorkloadFile = sys.argv[7];
    pathResultFile = sys.argv[8];
    # Check validity input parameters
    if(runtimeBenchmarkInSeconds <= 0 ):
        printUsageAndExit('Illegal runtime of benchmark argument');
    if(removeTimeInSeconds < 0 or removeTimeInSeconds > runtimeBenchmarkInSeconds):
        printUsageAndExit('Illegal remove at argument');
    if(addTimeInSeconds < 0 or addTimeInSeconds > runtimeBenchmarkInSeconds):
        printUsageAndExit('Illegal add at argument');
    # Clear database
    deleteAllDataInRiak(ipsInCluster);
    # Load database
    loadCommand = getLoadCommand(RIAK_BINDING, pathToWorkloadFile);
#     loadCommand = [PATH_YCSB_EXECUTABLE, 'load', RIAK_BINDING];
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
    runCommand = getRunCommand(RIAK_BINDING, pathToWorkloadFile, runtimeBenchmarkInSeconds);
#     runCommand = [PATH_YCSB_EXECUTABLE, 'run', RIAK_BINDING]; 
#     runCommand.extend(['-P', pathToWorkloadFile]); 
#     runCommand.extend(['-p', 'recordcount=' + str(RECORD_COUNT)]); 
#     runCommand.extend(['-p', 'operationcount=' + str(OPERATION_COUNT)]); 
#     runCommand.extend(['-p', 'measurementtype=timeseries']); 
#     runCommand.extend(['-p', 'timeseries.granularity=' + str(TIMESERIES_GRANULARITY)]);
#     runCommand.extend(['-p', 'maxexecutiontime=' + str(runtimeBenchmarkInSeconds), '-s']);
    print "Starting benchmark";
    benchmarkThread = Thread(target=executeCommandOnYcsbNodes, args=(runCommand, runCommand, pathResultFile, ['172.16.33.10']));
    benchmarkThread.start();
    # Remove node at "remove at"
    sleep(removeTimeInSeconds);
    print "Removing riak node from cluster: " + IpNodeToBeRemoved;
    killRiakNode(IpNodeToBeRemoved);
    # add node at "add at"
    sleep(addTimeInSeconds - removeTimeInSeconds);
    print "Adding riak node to cluster: " + IpNodeToBeRemoved;
    startRiakNode(IpNodeToBeRemoved, seedIp);
    # Wait for benchmark to finish and close result file
    benchmarkThread.join();
    # Plot results
    parseAndPlot(pathResultFile);

def startRiakNode(ip, seedIp):
    commandToExecute = "su riak -c 'riak start; riak-admin cluster join riak@" + seedIp + "; riak-admin cluster plan; riak-admin cluster commit'";
    executeCommandOverSsh(ip, commandToExecute);

def killRiakNode(ip):
    commandToExecute = "su riak -c 'riak-admin cluster leave riak@" + ip + "; riak-admin cluster plan; riak-admin cluster commit'";
    executeCommandOverSsh(ip, commandToExecute);

def printUsageAndExit(errorMessage):
    print 'Usage: script <IP node to be removed> <Seed Ip> <Ips in cluster> <runtime of benchmark (min)> <remove at (min)> <add at (min)> <Path to workload file> <path result file>';
    exit();

main();