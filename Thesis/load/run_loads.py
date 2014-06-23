#!/bin/python

import subprocess;
import time;
from Thesis.load.process_result.AggregatedBenchmarkResult import AggregatedBenchmarkResult; 
from Thesis.delete_data.deleteAllCouchdbData import deleteAllDataInCouchdb;
from Thesis.delete_data.deleteAllRiakData import deleteAllDataInRiak;

ipAddressMySqlMasterNode = "172.16.33.15";
pathForWorkloadFile = "/root/YCSB/workloads/workload_load";
cassandramysqlIps = ['172.16.33.15', '172.16.33.16'];
riakcouchdbIps = ['172.16.33.13', '172.16.33.14'];
otherYcsbNodes = ['172.16.33.10', '172.16.33.11', '172.16.33.12'];
CASSANDRA_CLI_CMD = 'cassandra-cli -f ';

def writeWorkloadFile(amountOfOperations, ipsInCluster):
    dataToWrite = 'recordcount=1000\n' + \
    'operationcount=' + amountOfOperations + "\n" + \
    """workload=com.yahoo.ycsb.workloads.CoreWorkload
    
readallfields=true
    
readproportion=0.6
updateproportion=0.4
scanproportion=0
insertproportion=0.4
 
requestdistribution=zipfian

hosts=""" + ",".join(ipsInCluster);
    f = open(pathForWorkloadFile, "w");
    f.write(dataToWrite);
    f.close();
    for ip in otherYcsbNodes:
        exitCode = subprocess.call(['scp', pathForWorkloadFile, 'root@' + ip + ':' + pathForWorkloadFile]);
        checkExitCode(exitCode);
        
def writeMySqlWorkloadFile(amountOfOperations, ipsInCluster):
    dataToWrite = 'recordcount=1000\n' + \
    'operationcount=' + amountOfOperations + "\n" + \
    """workload=com.yahoo.ycsb.workloads.CoreWorkload
    
readallfields=true
    
readproportion=0.6
updateproportion=0.4
scanproportion=0
insertproportion=0.4
 
requestdistribution=zipfian

hosts=""" + ",".join(ipsInCluster);
    f = open(pathForWorkloadFile, "w");
    f.write(dataToWrite);
    f.close();
    # Keep track of difference in operation distribution
    amountOfOperations = str(int(amountOfOperations)+15000);
    otherDataToWrite = 'recordcount=1000\n' + \
    'operationcount=' + amountOfOperations + "\n" + \
    """workload=com.yahoo.ycsb.workloads.CoreWorkload
    
readallfields=true
    
readproportion=0.5
updateproportion=0.5
scanproportion=0
insertproportion=0
 
requestdistribution=zipfian

hosts=""" + ",".join(ipsInCluster);
    f = open("/tmp/workload_load", "w");
    f.write(otherDataToWrite);
    f.close();
    for ip in otherYcsbNodes:
        exitCode = subprocess.call(['scp', '/tmp/workload_load', 'root@' + ip + ':' + pathForWorkloadFile]);
        checkExitCode(exitCode);
        
def checkExitCode(exitCode):
    if exitCode != 0:
        raise Exception("non-zero exitcode: " + str(exitCode));

def runRiak(opsPerSec, amountThreads, amountOfMachines):
    writeWorkloadFile('10000000', riakcouchdbIps);
    deleteAllDataInRiak(riakcouchdbIps);
    exitCode = subprocess.call(['bin/ycsb', 'load', 'riak', '-P', 'workloads/workload_load', '-s']);
    checkExitCode(exitCode);
    resultFileName = 'loads/riak/' + amountOfMachines + "_machines_" + amountThreads + '_thread_' + opsPerSec + 'opss';
    f = open(resultFileName, "w");
    command = ['/root/YCSB/bin/ycsb', 'run', 'riak', '-P', '/root/YCSB/workloads/workload_load', '-p', 'measurementtype=timeseries', '-p', 'timeseries.granularity=2000', '-target', opsPerSec, '-threads', amountThreads, '-p', 'maxexecutiontime=600', '-s'];
    executeCommandOnYcsbNodes(command, amountOfMachines, f);
    f.close();
    return (aggregateResults(otherYcsbNodes[0:int(amountOfMachines)-1], resultFileName), 'loads/riak/');

def runCouchdb(opsPerSec, amountThreads, amountOfMachines):
    writeWorkloadFile('10000000', riakcouchdbIps);
    deleteAllDataInCouchdb(riakcouchdbIps, 'usertable');
    exitCode = subprocess.call(['bin/ycsb', 'load', 'couchdb', '-P', 'workloads/workload_load', '-s']);
    checkExitCode(exitCode);
    resultFileName = 'loads/couchdb/' + amountOfMachines + "_machines_" + amountThreads + '_thread_' + opsPerSec + 'opss';
    f = open(resultFileName, "w");
    command = ['/root/YCSB/bin/ycsb', 'run', 'couchdb', '-P', '/root/YCSB/workloads/workload_load', '-p', 'measurementtype=timeseries', '-p', 'timeseries.granularity=2000', '-target', opsPerSec, '-threads', amountThreads, '-p', 'maxexecutiontime=600', '-s'];
    executeCommandOnYcsbNodes(command, amountOfMachines, f);
    f.close();
    return (aggregateResults(otherYcsbNodes[0:int(amountOfMachines)-1], resultFileName), 'loads/couchdb/');

def runMySQL(opsPerSec, amountThreads, amountOfMachines):
    writeMySqlWorkloadFile('10000000', cassandramysqlIps);
    exitCode = subprocess.call(['ssh', 'root@' + ipAddressMySqlMasterNode, 'mysql -u root -e "delete from ycsb_database.usertable;"']);
    checkExitCode(exitCode);
    exitCode = subprocess.call(['bin/ycsb', 'load', 'jdbc', '-P', 'workloads/workload_load', '-P', '/root/YCSB/jdbc/db_properties', '-s']);
    checkExitCode(exitCode);
    resultFileName = 'loads/mysql/' + amountOfMachines + "_machines_" + amountThreads + '_thread_' + opsPerSec + 'opss';
    f = open(resultFileName, "w");
    command = ['/root/YCSB/bin/ycsb', 'run', 'jdbc', '-P', '/root/YCSB/workloads/workload_load', '-P', '/root/YCSB/jdbc/db_properties', '-p', 'measurementtype=timeseries', '-p', 'timeseries.granularity=2000', '-target', opsPerSec, '-threads', amountThreads, '-p', 'maxexecutiontime=600', '-s'];
    executeCommandOnYcsbNodes(command, amountOfMachines, f);
    f.close();
    return (aggregateResults(otherYcsbNodes[0:int(amountOfMachines)-1], resultFileName), 'loads/mysql/');

def runCassandra(opsPerSec, amountThreads, amountOfMachines):
    writeWorkloadFile('1000000000', cassandramysqlIps);
    clearCassandraColumnFamily();
    exitCode = subprocess.call(['bin/ycsb', 'load', 'cassandra-10', '-P', 'workloads/workload_load', '-s']);
    checkExitCode(exitCode);
    resultFileName = 'loads/cassandra/' + amountOfMachines + "_machines_" + amountThreads + '_thread_' + opsPerSec + 'opss';
    f = open(resultFileName, "w");
    command = ['/root/YCSB/bin/ycsb', 'run', 'cassandra-10', '-P', '/root/YCSB/workloads/workload_load', '-p', 'measurementtype=timeseries', '-p', 'timeseries.granularity=2000', '-target', opsPerSec, '-threads', amountThreads, '-p', 'maxexecutiontime=600', '-s'];
    executeCommandOnYcsbNodes(command, amountOfMachines, f);
    f.close();
    return (aggregateResults(otherYcsbNodes[0:int(amountOfMachines)-1], resultFileName), 'loads/cassandra/');

def clearCassandraColumnFamily():
    clearCommand = '"use usertable;\n truncate data;\n quit;\n"';
    exitCode = subprocess.call(['ssh', 'root@' + cassandramysqlIps[0], 'echo ' + clearCommand + '>/tmp/cassandra_clear_command']);
    checkExitCode(exitCode);
    exitCode = subprocess.call(['ssh', 'root@' + cassandramysqlIps[0], CASSANDRA_CLI_CMD + '/tmp/cassandra_clear_command']);
    checkExitCode(exitCode);
    exitCode = subprocess.call(['ssh', 'root@' + cassandramysqlIps[0], 'rm -f /tmp/cassandra_clear_command']);
    checkExitCode(exitCode);

def executeCommandOnYcsbNodes(command, amountOfMachines, outputFile):
    listOfProcesses = [];
    localProcess = subprocess.Popen(command, stdout=outputFile);
    listOfProcesses.append(localProcess); 
    for i in range(0, int(amountOfMachines)-1):
        ipRemoteMachine = otherYcsbNodes[i];
        remoteCommand = " ".join(command) + '> /root/YCSB/result';
        process = subprocess.Popen(['ssh', 'root@' + ipRemoteMachine, remoteCommand]);
        listOfProcesses.append(process);
    while containsUnfinishedProcess(listOfProcesses):
        time.sleep(5);
    checkExitCodeOfProcesses(listOfProcesses);    

def checkExitCodeOfProcesses(listOfProcesses):
    for process in listOfProcesses:
        if process.poll() != 0:
            raise Exception("non-zero exitcode: " + str(process.poll()));

def containsUnfinishedProcess(listOfProcesses):
    for process in listOfProcesses:
        if process.poll() is None:
            return True;
    return False;

def runTests(runFunction, listOfOpsPerSec, listOfAmountThreads, listOfAmountOfMachines):
    for amountOfMachines in listOfAmountOfMachines:
        for amountOfThreads in listOfAmountThreads:
            aggResults = [];
            for opsPerSec in listOfOpsPerSec:
                (newResult,dirForResult) = runFunction(opsPerSec, amountOfThreads, amountOfMachines);
                aggResults.append(newResult);
            resultFileName = dirForResult + amountOfMachines + '_machines_' + amountOfThreads + '_thread_RESULT';
            printMergedAggResultsToFile(aggResults, resultFileName);

def aggregateResults(ipsRemoteYcsbClient, pathResultFile):
    resultPaths = copyResultFilesToLocal(ipsRemoteYcsbClient, pathResultFile);
    resultPaths.append(pathResultFile);
    return AggregatedBenchmarkResult(resultPaths);

def copyResultFilesToLocal(listOfIps, remotePath):
    pathsNewCopiedFiles = [];
    for ip in listOfIps:
        pathNewLocalFile = remotePath + '_' + ip;
        pathsNewCopiedFiles.append(pathNewLocalFile);
        exitCode = subprocess.call(['scp', 'root@' + ip + ':/root/YCSB/result', pathNewLocalFile]);
        checkExitCode(exitCode);
    return pathsNewCopiedFiles;

def printMergedAggResultsToFile(listOfAggResults, pathResultFile):
    f = open(pathResultFile, 'w');
    for operation in ['AverageReadLatency', 'AverageInsertLatency', 'AverageUpdateLatency', 
                      'AverageScanLatency', 'AverageDeleteLatency']:
        f.write('=== ' + operation + ' ===\n');
        for aggResult in listOfAggResults:
            f.write(str(aggResult.getThroughput()) + ', ' + str(aggResult.getAggregatedLatency(operation)) + '\n');
    f.close();

#def main():
    
#     # Couchdb 1 machine
#     runCouchdb('5', '1', '1');
#     runCouchdb('10', '1', '1');
#     runCouchdb('15', '1', '1');
#     runCouchdb('20', '1', '1');
#     runCouchdb('1000000', '1', '1');
#     # Couchdb 2 machines
#     runCouchdb('25', '10', '1');
#     runCouchdb('50', '10', '1');
#     runCouchdb('100', '10', '1');
#     runCouchdb('150', '10', '1');
#     runCouchdb('1000000', '10', '1');
#     # Couchdb 3 machines
#     runCouchdb('25', '50', '1');
#     runCouchdb('50', '50', '1');
#     runCouchdb('100', '50', '1');
#     runCouchdb('150', '10', '1');
#     runCouchdb('1000000', '10', '1');
#     # Couchdb 4 machines
#     runCouchdb('25', '50', '1');
#     runCouchdb('50', '50', '1');
#     runCouchdb('100', '50', '1');
#     runCouchdb('150', '50', '1');
#     runCouchdb('1000000', '50', '1');
#     
#     runCouchdb('25', '100', '1');
#     runCouchdb('50', '100', '1');
#     runCouchdb('100', '100', '1');
#     runCouchdb('150', '100', '1');
#     runCouchdb('1000000', '100', '1');
#     
#     runCouchdb('25', '500', '1');
#     runCouchdb('50', '500', '1');
#     runCouchdb('100', '500', '1');
#     runCouchdb('150', '500', '1');
#     runCouchdb('1000000', '500', '1');



#     # MySQL 1 machine
#     runMySQL('25', '15000', '10', '1');
#     runMySQL('50', '30000', '10', '1');
#     runMySQL('100', '65000', '10', '1');
#     runMySQL('1500', '80000', '10', '1');
#     # MySQL 2 machines
#     runMySQL('25', '15000', '10', '2');
#     runMySQL('50', '30000', '10', '2');
#     runMySQL('100', '65000', '10', '2');
#     runMySQL('1500', '80000', '10', '2');
#     # MySQL 3 machines
#     runMySQL('25', '15000', '10', '3');
#     runMySQL('50', '30000', '10', '3');
#     runMySQL('100', '65000', '10', '3');
#     runMySQL('1500', '80000', '10', '3');
#     # MySQL 4 machines
#     runMySQL('25', '15000', '10', '4');
#     runMySQL('50', '30000', '10', '4');
#     runMySQL('100', '65000', '10', '4');
#     runMySQL('1500', '80000', '10', '4');
#     
#     # Riak 1 machine
#     runRiak('100', '60000', '10', '1');
#     runRiak('200', '120000', '10', '1');
#     runRiak('300', '180000', '10', '1');
#     runRiak('4000', '240000', '10', '1');
#     # Riak 2 machines
#     runRiak('100', '60000', '10', '2');
#     runRiak('200', '120000', '10', '2');
#     runRiak('250', '150000', '10', '2');
#     runRiak('3000', '180000', '10', '2');
#     # Riak 3 machines
#     runRiak('50', '30000', '10', '3');
#     runRiak('100', '60000', '10', '3');
#     runRiak('150', '90000', '10', '3');
#     runRiak('2000', '130000', '10', '3');
#     # Riak 4 machines
#     runRiak('50', '30000', '10', '4');
#     runRiak('100', '60000', '10', '4');
#     runRiak('150', '90000', '10', '4');
#     runRiak('2000', '130000', '10', '4');
    
#     runTests(runRiak, ['100', '200', '300', '400', '1000000'], ['1'], ['1']);
#     runTests(runRiak, ['100', '200', '300', '400', '1000000'], ['10', '25', '50', '100'], ['1']);
#     runTests(runRiak, ['100', '200', '300', '400', '1000000'], ['10'], ['1', '2', '3', '4']);
#     
#     runTests(runCassandra, ['10'], ['1'], ['2']);
    
#     runTests(runCassandra, ['2', '5', '7', '9', '1000000000'], ['1'], ['1']);
#     runTests(runCassandra, ['2', '5', '7', '10', '1000000000'], ['25', '50', '100', '250', '500'], ['1']);

    
#     # Cassandra 1 machine
#     runCassandra('1000', '600000', '10', '1');
#     runCassandra('1500', '900000', '10', '1');
#     runCassandra('2000', '1200000', '10', '1');
#     runCassandra('2000000', '2000000', '10', '1');
#     # Cassandra 2 machines
#     runCassandra('200', '120000', '10', '2');
#     runCassandra('500', '300000', '10', '2');
#     runCassandra('1000', '600000', '10', '2');
#     runCassandra('2000000', '1200000', '10', '2');
#     # Cassandra 3 machines
#     runCassandra('200', '120000', '10', '3');
#     runCassandra('500', '300000', '10', '3');
#     runCassandra('1000', '600000', '10', '3');
#     runCassandra('1600000', '1600000', '10', '3');
#     # Cassandra 4 machines
#     runCassandra('200', '120000', '10', '4');
#     runCassandra('400', '240000', '10', '4');
#     runCassandra('800', '480000', '10', '4');
#     runCassandra('1600000', '1600000', '10', '4');

# main();