import time;
import subprocess;
import json;

def deleteAllDataInCouchdb(ipsInCluster, database):
    # Wait for replication to finish
    time.sleep(60);
    jsonObj = retrieveDocumentsAsJson(ipsInCluster, database);
    commands = getHttpDeleteRequests(jsonObj, ipsInCluster, database);
    executeDeletionInBatch(commands);
    time.sleep(60);
    compactDatabase(ipsInCluster, database);

# Execute compaction, to reduce disk usage. This in not automatic by default
def compactDatabase(ipsInCluster, database):
    for ip in ipsInCluster:
        exitCode = subprocess.call('curl -H "Content-Type:application/json" -X POST  http://' + ip + ':5984/' + database + '/_compact', shell=True);
        checkExitCodeOfProcess(exitCode, 'Executing compaction failed on server: ' + ip);
    # Wait for compaction to finish
    time.sleep(600);

# Delete data in batches of 9000 documents.
# 100 processes with 90 sequential document deletions 
# of single connection per process
# This reduces cost of handshaking.
def executeDeletionInBatch(commands):
    processes = [];
    counter = 0;
    for i in range(0, len(commands), 90):
        baseCommand = ['curl', '-XDELETE'];
        baseCommand.extend(commands[i:i+90]);
        process = subprocess.Popen(baseCommand);
        processes.append(process);
        counter += 1;
        if counter%100 == 0:
                waitForProcessesToEnd(processes);
                processes = [];

def retrieveDocumentsAsJson(ipsInCluster, database):
    searchProcess = subprocess.Popen(['curl', '-XGET', 'http://' + ipsInCluster[0] + ':5984/' + database + '/_all_docs'], stdout=subprocess.PIPE);
    (stdout, _) = searchProcess.communicate();
    return json.loads(stdout);

# Create http delete request for every document.
def getHttpDeleteRequests(jsonObj, ipsInCluster, database):
    commands = [];
    for doc in jsonObj['rows']:
        key = doc['key'];
        revision = doc['value']['rev'];
        commands.append(ipsInCluster[0] + ':5984/' + database + '/' + key + '?rev=' + revision);
    return commands;
        
def waitForProcessesToEnd(listOfProcesses):
        for process in listOfProcesses:
                process.wait();

def checkExitCodeOfProcess(exitCode, errorMessage):
    if exitCode != 0:
        raise Exception(errorMessage + ' (exitcode: ' + str(exitCode) + ')');